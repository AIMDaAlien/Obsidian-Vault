# Subagent Implementation Guide

> **Practical guide for implementing remaining features using Claude Code Web subagents**

## 📋 Overview

**Current Status:** MVP Complete (Adaptive AI + Offline Mode working)

**Remaining Work:** 4 major features requiring 11-15 hours total

**Tools:**
- Claude Code Web (primary) - Subagent orchestration
- shadcn/ui - Component library
- Context7 - Documentation access

---

## 🎯 Subagent Workflow

### Setup
1. Open Claude Code Web
2. Clone: `git clone https://github.com/AIMDaAlien/local-keebspeed.git`
3. Verify build: `npm install && npm run dev`
4. Create feature branch for each subagent

### Work Pattern
```
Subagent 1 (Storage) → feature/storage-persistence
Subagent 2 (Settings) → feature/settings-panel
Subagent 3 (Keyboard) → feature/keyboard-visual
Subagent 4 (Progress) → feature/progress-ui

Each branch:
  1. Implement feature
  2. Test locally
  3. Commit
  4. Push
  5. Create PR
  6. Review in main session
  7. Merge to main
```

---

## 🗂 Subagent 1: Storage Persistence

**Priority:** CRITICAL (needed by others)
**Time:** 3-4 hours
**Confidence:** 95%

### Tasks

#### 1. User Profile Hook
**File:** `src/hooks/useUserProfile.ts`

**Purpose:** Initialize and manage user profile

**Implementation:**
```typescript
import { useState, useEffect } from 'react';
import { getUserProfile, createUserProfile } from '@/lib/storage/operations';

export const useUserProfile = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initProfile();
  }, []);

  const initProfile = async () => {
    let userId = localStorage.getItem('typinglab-user-id');
    
    if (!userId) {
      userId = crypto.randomUUID();
      localStorage.setItem('typinglab-user-id', userId);
      
      const newProfile: UserProfile = {
        id: userId,
        targetWPM: 35,
        currentLevel: 0,
        activeLetters: [],
        masteredLetters: [],
        createdAt: new Date(),
        lastSession: new Date(),
      };
      
      await createUserProfile(newProfile);
      setProfile(newProfile);
    } else {
      const existing = await getUserProfile(userId);
      setProfile(existing);
    }
    
    setIsLoading(false);
  };

  return { profile, isLoading, refreshProfile: initProfile };
};
```

#### 2. Wire Session Saving
**File:** `src/hooks/useTypingEngine.ts` (modify)

**Add to onComplete:**
```typescript
const session: Session = {
  id: crypto.randomUUID(),
  userId: profile!.id,
  timestamp: new Date(),
  duration: metrics.timeElapsed * 1000,
  grossWPM: calculateWPM(metrics.charactersTyped, metrics.timeElapsed * 1000),
  netWPM: metrics.currentWPM,
  accuracy: metrics.currentAccuracy / 100,
  keyStats: extractPerKeyStats(keystrokesRef.current),
  bigramStats: [],
  text: currentLesson,
  targetText: currentLesson,
  errorCount: metrics.errorsCount,
  completionRate: currentIndex / currentLesson.length,
};

await saveSession(session);
```

#### 3. Session History Component
**File:** `src/components/SessionHistory.tsx`

**Install shadcn components:**
```bash
npx shadcn@latest add card scroll-area
```

**Component:**
```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

export const SessionHistory = ({ userId }: { userId: string }) => {
  const [sessions, setSessions] = useState<Session[]>([]);
  
  useEffect(() => {
    loadSessions();
  }, [userId]);
  
  const loadSessions = async () => {
    const history = await getSessionHistory(userId, 10);
    setSessions(history);
  };
  
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Recent Sessions</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[400px]">
          {sessions.map((session) => (
            <div key={session.id} className="flex justify-between border-b py-3 px-2">
              <span className="font-mono text-lg font-bold" style={{ color: '#E6E6FA' }}>
                {session.netWPM} WPM
              </span>
              <span className="text-neutral-400">
                {(session.accuracy * 100).toFixed(1)}%
              </span>
              <span className="text-xs text-neutral-500">
                {new Date(session.timestamp).toLocaleDateString()}
              </span>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
    </Card>
  );
};
```

#### 4. Export/Import
**File:** `src/components/DataManagement.tsx`

```tsx
import { Button } from '@/components/ui/button';
import { exportAllData, importData } from '@/lib/storage/export';

export const DataManagement = ({ userId }: { userId: string }) => {
  const handleExport = async () => {
    const jsonData = await exportAllData(userId);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `typinglab-export-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };
  
  const handleImport = async (file: File) => {
    const text = await file.text();
    await importData(text);
    window.location.reload();
  };
  
  return (
    <div className="space-y-3">
      <Button onClick={handleExport} variant="outline" className="w-full">
        📥 Export All Data
      </Button>
      <input
        type="file"
        accept=".json"
        onChange={(e) => e.target.files?.[0] && handleImport(e.target.files[0])}
        className="hidden"
        id="import-file"
      />
      <Button 
        onClick={() => document.getElementById('import-file')?.click()}
        className="w-full"
      >
        📤 Import Data
      </Button>
    </div>
  );
};
```

### Testing
```bash
# 1. Complete a session
npm run dev
# Type a lesson, complete it

# 2. Reload page
Cmd+R / Ctrl+R

# 3. Verify persistence
# Check DevTools → Application → IndexedDB → typinglab-db
# Should see session record

# 4. Test export
# Click export button
# Verify JSON file downloads

# 5. Test import
# Clear localStorage and IndexedDB
# Import the exported file
# Verify data restored
```

---

## ⚙️ Subagent 2: Settings Panel

**Priority:** HIGH
**Time:** 3-4 hours
**Confidence:** 93%

### Tasks

#### 1. Install Components
```bash
npx shadcn@latest add dialog drawer button slider switch label
```

#### 2. Settings Hook
**File:** `src/hooks/useSettings.ts`

```typescript
import { useState, useEffect } from 'react';
import { getSettings, saveSettings } from '@/lib/storage/operations';

export const useSettings = (userId: string) => {
  const [settings, setSettings] = useState<AppSettings>({
    theme: 'dark',
    soundEnabled: false,
    showKeyboard: true,
    showHands: false,
    targetWPM: 35,
    language: 'en',
    fontSize: 'medium',
  });

  useEffect(() => {
    loadSettings();
  }, [userId]);

  const loadSettings = async () => {
    const saved = await getSettings(userId);
    if (saved) setSettings(saved);
  };

  const updateSetting = async <K extends keyof AppSettings>(
    key: K,
    value: AppSettings[K]
  ) => {
    const updated = { ...settings, [key]: value };
    setSettings(updated);
    await saveSettings(userId, updated);
  };

  return { settings, updateSetting };
};
```

#### 3. Responsive Dialog/Drawer
**File:** `src/components/Settings.tsx`

**Use shadcn/ui responsive pattern:**
```tsx
import { useState } from 'react';
import { useMediaQuery } from '@/hooks/use-media-query';
import { Settings as SettingsIcon } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from '@/components/ui/drawer';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';

export const Settings = ({ settings, updateSetting }: any) => {
  const [open, setOpen] = useState(false);
  const isDesktop = useMediaQuery('(min-width: 768px)');

  const SettingsForm = () => (
    <div className="space-y-6 py-4 px-2">
      {/* Target WPM */}
      <div className="space-y-2">
        <Label>Target WPM: {settings.targetWPM}</Label>
        <Slider
          value={[settings.targetWPM]}
          onValueChange={([value]) => updateSetting('targetWPM', value)}
          min={10}
          max={100}
          step={5}
          className="w-full"
        />
        <p className="text-xs text-neutral-500">
          Keys unlock when you reach this speed consistently
        </p>
      </div>

      {/* Sound Effects */}
      <div className="flex items-center justify-between">
        <div className="space-y-0.5">
          <Label htmlFor="sound">Sound Effects</Label>
          <p className="text-xs text-neutral-500">
            Audio feedback on keystrokes
          </p>
        </div>
        <Switch
          id="sound"
          checked={settings.soundEnabled}
          onCheckedChange={(checked) => updateSetting('soundEnabled', checked)}
        />
      </div>

      {/* Show Keyboard */}
      <div className="flex items-center justify-between">
        <div className="space-y-0.5">
          <Label htmlFor="keyboard">Show Keyboard</Label>
          <p className="text-xs text-neutral-500">
            Visual keyboard display
          </p>
        </div>
        <Switch
          id="keyboard"
          checked={settings.showKeyboard}
          onCheckedChange={(checked) => updateSetting('showKeyboard', checked)}
        />
      </div>

      {/* Reset Data */}
      <div className="pt-4 border-t border-neutral-800">
        <Button
          variant="destructive"
          onClick={() => {
            if (confirm('Clear all data? This cannot be undone.')) {
              localStorage.clear();
              indexedDB.deleteDatabase('typinglab-db');
              window.location.reload();
            }
          }}
          className="w-full"
        >
          🗑️ Reset All Data
        </Button>
      </div>
    </div>
  );

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" size="icon">
            <SettingsIcon className="h-5 w-5" />
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Settings</DialogTitle>
          </DialogHeader>
          <SettingsForm />
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer open={open} onOpenChange={setOpen}>
      <DrawerTrigger asChild>
        <Button variant="outline" size="icon">
          <SettingsIcon className="h-5 w-5" />
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader className="text-left">
          <DrawerTitle>Settings</DrawerTitle>
        </DrawerHeader>
        <SettingsForm />
      </DrawerContent>
    </Drawer>
  );
};
```

#### 4. Media Query Hook
**File:** `src/hooks/use-media-query.ts`

```typescript
import { useState, useEffect } from 'react';

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [query]);

  return matches;
}
```

### Testing
```bash
# Desktop test
1. Open on laptop (>768px width)
2. Click settings icon
3. Verify Dialog opens (modal overlay)

# Mobile test
4. Resize to <768px
5. Click settings icon
6. Verify Drawer opens (slides from bottom)

# Functionality test
7. Adjust target WPM slider
8. Toggle switches
9. Reload page
10. Verify settings persisted
```

---

## ⌨️ Subagent 3: Keyboard Visualization

**Priority:** MEDIUM
**Time:** 3-4 hours
**Confidence:** 90%

### Task

**File:** `src/components/KeyboardDisplay.tsx`

```tsx
import { cn } from '@/lib/utils';

const KEYBOARD_LAYOUT = [
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
  ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
];

interface KeyboardDisplayProps {
  activeKeys: string[];
  targetKey?: string;
  className?: string;
}

export const KeyboardDisplay: React.FC<KeyboardDisplayProps> = ({
  activeKeys,
  targetKey,
  className,
}) => {
  const activeSet = new Set(activeKeys.map(k => k.toLowerCase()));
  
  return (
    <div className={cn('space-y-2', className)}>
      {KEYBOARD_LAYOUT.map((row, rowIdx) => (
        <div key={rowIdx} className="flex justify-center gap-2">
          {row.map((key) => {
            const isActive = activeSet.has(key);
            const isTarget = key === targetKey?.toLowerCase();
            
            return (
              <div
                key={key}
                className={cn(
                  'w-10 h-10 sm:w-12 sm:h-12 rounded flex items-center justify-center',
                  'font-mono text-sm sm:text-lg font-semibold transition-all duration-200',
                  isTarget && 'animate-pulse ring-2 scale-110',
                  isActive 
                    ? 'bg-[#E6E6FA] text-[#171717] ring-[#E6E6FA]' 
                    : 'bg-neutral-800 text-neutral-600'
                )}
              >
                {key === ' ' ? '␣' : key.toUpperCase()}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};
```

### Integration

**In `src/App.tsx`:**
```tsx
import { KeyboardDisplay } from './components/KeyboardDisplay';

// In typing interface section:
{settings.showKeyboard && (
  <KeyboardDisplay
    activeKeys={activeKeys}
    targetKey={currentLesson[currentIndex]}
    className="mt-8"
  />
)}
```

### Testing
```bash
# Visual test
1. Start typing session
2. Verify keyboard displays
3. Check active keys highlighted in lavender
4. Confirm target key pulses

# Responsive test
5. Resize window
6. Verify keys scale appropriately
7. Check mobile layout (stacked)
```

---

## 📊 Subagent 4: Progress Tracking

**Priority:** MEDIUM
**Time:** 2-3 hours
**Confidence:** 87%

### Tasks

#### 1. Install Components
```bash
npx shadcn@latest add progress badge
```

#### 2. Key Confidence Component
**File:** `src/components/KeyConfidence.tsx`

```tsx
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

export const KeyConfidence = ({ stats }: { stats: KeyStats[] }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((keyStat) => (
        <div key={keyStat.letter} className="space-y-2 bg-neutral-800 rounded-lg p-3">
          <div className="flex justify-between items-center">
            <span className="font-mono font-bold text-xl">{keyStat.letter.toUpperCase()}</span>
            <Badge 
              variant={keyStat.confidence >= 1.0 ? 'default' : 'secondary'}
              style={keyStat.confidence >= 1.0 ? { backgroundColor: '#E6E6FA', color: '#171717' } : {}}
            >
              {keyStat.wpm} WPM
            </Badge>
          </div>
          <Progress value={keyStat.confidence * 100} className="h-2" />
          <div className="flex justify-between text-xs text-neutral-500">
            <span>{(keyStat.accuracy * 100).toFixed(0)}% acc</span>
            <span>{keyStat.attempts} tries</span>
          </div>
        </div>
      ))}
    </div>
  );
};
```

#### 3. Unlock Progress
**File:** `src/components/UnlockProgress.tsx`

```tsx
export const UnlockProgress = ({ 
  activeKeys, 
  nextKey 
}: { 
  activeKeys: KeyStats[]; 
  nextKey: string | null;
}) => {
  const allReady = activeKeys.every(k => 
    k.wpm >= 35 && k.accuracy >= 0.95 && k.attempts >= 20
  );

  if (!nextKey) {
    return (
      <div className="text-center p-6 bg-green-500/10 rounded-lg border border-green-500/20">
        <div className="text-4xl mb-2">🎉</div>
        <h3 className="font-bold text-green-500">All keys mastered!</h3>
      </div>
    );
  }

  return (
    <div className="bg-neutral-800 rounded-lg p-4">
      <h3 className="font-bold mb-2" style={{ color: '#C8A2C8' }}>
        Next Key: <span className="font-mono text-2xl ml-2">{nextKey.toUpperCase()}</span>
      </h3>
      {allReady ? (
        <p className="text-green-500">✅ Ready to unlock!</p>
      ) : (
        <div className="space-y-2">
          <p className="text-neutral-400 text-sm">Keep practicing current keys:</p>
          <ul className="text-xs text-neutral-500 space-y-1">
            {activeKeys.filter(k => k.wpm < 35 || k.accuracy < 0.95 || k.attempts < 20).map(k => (
              <li key={k.letter}>
                <span className="font-mono">{k.letter}</span>: {k.wpm}WPM, {(k.accuracy * 100).toFixed(0)}%, {k.attempts} tries
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
```

### Integration
Add to `App.tsx` in a new "Progress" tab or section.

---

## ✅ Success Criteria

### Subagent 1: Storage
- [ ] Sessions persist across reloads
- [ ] Export downloads valid JSON
- [ ] Import restores data correctly
- [ ] Works offline

### Subagent 2: Settings
- [ ] Desktop shows Dialog, mobile shows Drawer
- [ ] Settings persist
- [ ] Target WPM affects algorithm
- [ ] Reset clears data

### Subagent 3: Keyboard
- [ ] QWERTY layout displays
- [ ] Active keys highlighted
- [ ] Target key pulses
- [ ] Responsive on mobile

### Subagent 4: Progress
- [ ] Confidence bars per key
- [ ] Unlock indicator shows status
- [ ] Visual feedback on mastery

---

## 🎯 Final Integration Checklist

- [ ] All subagent branches merged
- [ ] Build succeeds: `npm run build`
- [ ] No TypeScript errors
- [ ] All features work together
- [ ] Offline mode verified
- [ ] Performance maintained (<16ms, 60fps)

---

**Related:**
- [[00 - TypingLab Project Overview]]
- [[02 - Implementation Journey]]
- [[07 - Testing and Verification]]

*Last Updated: November 18, 2025*
