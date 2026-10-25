---
type: note
category: Rig & Hardware
tags: [omarchy, rig-hardware, gpu, hardware]
updated: 2026-09-25
publish: true
created: 2026-09-25
machine: bigrig
title: "GPU Maxing / OC Research — Sept 2026 (rig: Z690-A DDR4, 13600K, RX 9060 XT 16GB, RTX 3060 12GB)"
---

# GPU Maxing / OC Research — Sept 2026 (rig: Z690-A DDR4, 13600K, RX 9060 XT 16GB, RTX 3060 12GB)

Verified live: RX 9060 XT negotiates PCIe 5.0 x16 (32 GT/s) — the 13600K CPU slot is doing its job.
RTX 3060: Gen3 x16 max, currently idling at Gen1 x4 (normal power-saving downshift; ramps under load).
Slot priority on Z690-A DDR4: full-length slots 1/4 = CPU (x16/x8/x4, Gen5 capable), slots 2/3/5 = chipset x4.

## 1. BIOS settings (F7 or later on MSI Z690-A DDR4)
- PCIe slot config: slot the 9060 XT is in → PCIe 5.0 speed, don't force Gen3. 3060 slot is Gen3-capped by the card itself.
- Above 4G Decoding: ENABLED (required for >4 GPU VRAM bars)
- Re-Size BAR Support: ENABLED (some LLM loads checkpoint faster)
- Resizable BAR aperture: Auto/1GB+ — llamacpp sometimes benefits from large BAR on Navi (iogpu_barsize equivalent). If BAR stays small (check `lspci -vv | grep -i 'BAR.*32bit\|prefetchable'`), large BAR helps.
- C-States: leave default; LLM serving is latency-sensitive in decode bursts but the 8080 llama-server is mostly GPU-bound. Disabling C1E/C3 can smooth spikes.
- Above-4G was the historically-breaking setting — confirm it's on (vBIOS update for the 3060 not needed; 3060 predates ReBAR official support).
- Intel adaptive boost / 13600K: irrelevant to GPU inference unless you run CPU offload (you don't — GPU-only mandate).

## 2. Overclocking the 9060 XT (Navi 44)
Two ways: `amdgpu` sysfs, or `lact` GUI daemon (https://github.com/ilya-zlobintsev/LACT — recommended, has an AUR package, live fan/vram/core curve control without X restarts).
- Core: stock ~2.4-2.9 GHz boost. +200-300 MHz core is typical headroom on Navi44; test stability with a llama-server decode-heavy run, not 3DMark (OC fails under sustained GPU compute).
- VRAM: Navi 44 memory stock 20 Gbps on the XT. Real-world headroom small; +8-15% via `memory_clock` sysfs or LACT slider if non-X. Since decode t/s is memory-bandwidth-bound, VRAM is the lever that actually moves tokens/sec, not core.
- Fan curve: 9060 XT 16GB runs hot under llama.cpp sustained load; set LACT curve to hit ~70-75% around 70°C so VRAM junction stays cool (thermal throttling = instant t/s drop).
- Stability check: `gpu=1 nvidia-smi -q -i 1` equivalent → `radeontop` + watch `vram_clock`/`mem_clock` in `amdgpu` sysfs; run llama-server decode benchmark before/after at fixed context.

## 3. Overclocking the 3060
- `nvidia-settings -a '[gpu:0]/GPUGraphicsClockOffsetAllPerformanceLevels=150'` and `GPUMemoryTransferRateOffsetAllPerformanceLevels=1000` (3060 responds well to +1000-1500 MB/s VRAM offset; large OC gains because it's GDDR6 not GDDR6X).
- Persistence mode + `nvidia-pm` or `nvidia-smi -pm 1` so clocks don't drop between requests.
- `cuda_gpuclock_offset` and `cuda_memclock_offset` in llama.cpp build flags as an alternative (llama.cpp supports OC flags at compile time — nvidia/cuda build: `-DGGML_CUDA_...`). Actually llama.cpp reads `GGML_CUDA_ENABLE_UNIFIED_MEMORY` etc, not OC. Skip — use nvidia-settings.
- Power limit: `nvidia-smi -pl 170` (3060 stock 170W). Under VRAM-bound LLM load, power isn't usually the limiter; leave it unless clocks sag.

## 4. llama.cpp / serving config for the two-GPU split
Current setup (memory): llama-server 8080 with MTP 128K ctx on Qwen3-27B Q5_K_M, deep 256K variant, both GPU-only.
- Layer split: `--n-gpu-layers` with `--split-mode row` vs `layer`. With a 16GB + 12GB pair and a 27B Q5_K_M (~19GB weights + KV), you have ~28GB usable across both — layer split puts fewer layers on the 3060 (the slow Gen3 + 12GB card) and it becomes the bottleneck for decode. Alternative: `--tensor-split 16,12` (proportional VRAM). Row-split requires NCCL, avoid — this is a mixed-vendor setup, no NVLink bridge between AMD+NVIDIA.
- Prefill speed lever: **batch size** (`-b`) and **ubatch** (`-ub`). Prefill is compute-bound: raise `-ub 2048` (or 4096 if VRAM allows) to saturate the 9060 XT compute. Default 512 is way too small for a 27B.
- Decode lever: KV cache quantization (`--cache-type-k q8_0 --cache-type-v q8_0`) doubles effective context for the same VRAM, minor quality loss, big t/s win at 128K/256K.
- Flash attention: `-fa` should already be on (MTP builds default) — confirm with `--verbose` on server startup.
- MTP (multi-token prediction) on the 27B: already in use (128K MTP). That's the biggest decode t/s lever and it's engaged.
- Inter-op threading: `-t` on 13600K = 6 P-cores worth (12 threads) for post-processing; server is GPU-bound so `-t 8` is plenty; oversubscribing hurts latency.
- `--no-mmap` / `--mlock`: pin the model in RAM to avoid page-in stalls at first token after idle.

## 5. Kernel / OS-level levers (Arch/Omarchy)
- `vm.max_map_count` raise (default 65530): llama.cpp mmaps many tensors — `sysctl vm.max_map_count=2147483642` (Arch default on many setups already higher). Add to sysctl.d.
- `amdgpu.ppfeaturemask=0xffffffff` kernel param (unlocks full PowerPlay OC sysfs, i.e. `pp_dpm_sclk`/`pp_od_clk_voltage` control) — required for deep OC via sysfs instead of LACT.
- NVMe/CPU governor: `performance` governor for CPU while serving (`cpupower frequency-set -g performance`), since decode token latency has a CPU-side tokenizer/detokenizer component.
- `vm.swappiness=10` and `vm.vfs_cache_pressure=50` to keep model pages resident.
- Disable `pcie_aspm` for GPU slots if link resets/retrains are visible (`dmesg | grep -i pcie` for AER errors) — usually not needed on desktop.

## 6. Verification plan (measure, don't guess)
1. `llama-server` launch with a fixed prompt set; benchmark decode t/s and prefill t/s via llama.cpp's built-in benchmark endpoint (`/v1/chat/completions` with `stream:false`, read `timings` from response).
2. Apply BIOS changes (Above4G/ReBAR/C-States) one at a time → re-benchmark.
3. LACT: VRAM OC on 9060 XT (+8% step) → re-benchmark. Then core OC +200 → re-benchmark.
4. nvidia-settings VRAM offset +1000 on 3060 → re-benchmark.
5. Change `-ub` 512→2048→4096 and measure prefill delta; this is usually a 2-4x prefill jump on big models.
6. KV cache q8_0 → measure decode t/s and effective-context ceiling.

## Reference: where the numbers come from
- PCIe link states verified live via nvidia-smi + amdgpu sysfs (this session).
- Z690-A DDR4 slot map from MSI manual; 9060 XT must be in a CPU-attached slot (verified Gen5, so it is).
- Navi44 OC ranges: community consensus, not measured on this rig yet.
