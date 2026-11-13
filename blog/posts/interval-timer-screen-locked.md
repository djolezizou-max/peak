---
title: "Interval Timer Stops When the Screen Locks"
seoTitle: "Interval Timer Stops When the Screen Locks"
description: "Your interval timer still pauses when the phone locks or you switch to Spotify. Here is which setting keeps an installed app cueing, including Peak Interval."
date: "2026-11-13"
featured_image: "/assets/blog/interval-timer-screen-locked.png"
image_alt: "A woman running on a city pavement at dawn with a phone in an armband, earbuds in, and light blue shoes"
layout: "post.liquid"
tags: "posts"
category: "App Features"
---

You lock the phone, slide it into an armband, and the next voice cue never comes. You unlock it and the round is stuck where you left it, or the clock has jumped ahead and the beeps in between are simply gone. The same thing happens when you open Spotify to skip a song: the Tabata waits until you come back.

That is a different failure from a browser timer. A tab that stalls once the screen locks is the problem in [online interval timer vs an app](/blog/posts/online-interval-timer). This one is an app you already installed. The clock and the cue stop for different reasons, and the setting you change depends on which of the two you actually have.

## Tell the two failures apart

Unlock the phone and look at the countdown before you change anything.

If the number is frozen on the second you locked it, or it leaps forward and you never heard the transitions, the app was suspended. The lock, or leaving the app, stopped the process that was counting.

If the countdown is exactly where it should be and you simply heard nothing, the clock ran the whole time. The cue was played as a notification sound, and the silent switch, a Focus mode, or Do Not Disturb swallowed it. A louder beep will not revive a suspended app, and turning the ringer up will not help a cue that already rides on the media volume.

Write down which of those two you saw. The rest of the fix follows from it.

## Why the lock suspends some timers

iOS and Android both treat an app you cannot see as idle, unless that app has told the system the workout has to keep going. Playing audio the way a music app does is the signal they honour. A countdown that only advances while its own screen is open stops when you press the side button.

When you open it again, a careful app rebuilds the time from the clock, so the number looks right and the cues you needed have already passed. A weaker one stays frozen until the next time it is on screen. Either way you trained without the boundaries you set.

Background App Refresh is the setting people try first, and it fetches occasional updates. A live countdown needs the system to treat the session as playback for the whole workout. On Android the visible sign of that is a notification that stays up until you stop. No notification, and the screen turning off is enough to freeze the clock. Battery saver and the phone maker's own cleaner can still stop an app that shows one. **Settings → Apps → [the timer] → Battery → Unrestricted** is the exemption that fixes most of those, and the [Android interval timer checklist](/blog/posts/interval-timer-app-android) is the five-minute version of that test on your own phone.

## Why opening Spotify pauses the round

Leaving the timer to change a track is the same event as locking it, when the app only runs in front. Spotify comes forward, the timer is suspended, and the interval waits.

A timer that holds a playback session keeps counting while another app is open. The cue should lower the music for a moment and hand it back, which is the setup in [interval timer with music](/blog/posts/interval-timer-with-music). If opening Spotify pauses the intervals themselves, the workout is not running in the background. Volume, ducking, and a different playlist leave that failure where it is.

A phone call is the one interruption the system always wins. iOS takes audio away for the length of the call. What you want when you hang up is the same phase and round you left, held where you paused, rather than a jump forward to match the wall clock.

## The settings that keep the cues going

On iPhone, cues played as media audio keep sounding with the ringer off and with a gym Focus on. If you want the phase on the glass without unlocking, the session belongs in a Live Activity: **Settings → [the timer] → Live Activities**. That control is how you read the countdown. The sound comes from the audio session, not from the Live Activity toggle.

On Android, the ongoing notification plus Battery set to Unrestricted is the pair that survives a locked screen. A timer that only lasts while the display is forced to stay on is one you hold in your hand. An armband needs the session to continue with the screen off.

Peak Interval keeps its audio cues playing with the phone locked. On iPhone the lock screen shows the current phase and countdown, and the skip control sits there too, so ending a set early does not mean unlocking with sweaty hands. Peak Interval's Apple Watch app taps at the end of each rest, which is a cue that does not depend on the phone speaker in a pocket. The [iPhone checklist](/blog/posts/interval-timer-iphone) is how to confirm the silent switch and Focus on your own phone before you trust a long run to it.

## Two minutes in the armband

Start six rounds of 20 seconds on and 10 seconds off. Lock the phone. Put it where you actually train, in the armband or a pocket, and do not touch it until the six rounds should be over.

Every change of phase should sound on time. When you unlock, the round on screen should be the one you just heard.

Then run it once more. With the phone locked and the timer going, open your music app, skip one track, and lock it again. The interval you were in should still be the interval you are in.

If the first check fails, the app is going idle with the screen. If the first check passes and the second one fails, leaving the app is what suspends it, and you need a timer that keeps its session while another app is in front. If both pass, you can run the repeats and look at the phone only when you choose to.
