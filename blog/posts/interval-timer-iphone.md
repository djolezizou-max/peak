---
title: "Interval Timer on iPhone: What to Test Before You Trust One With the Screen Locked"
seoTitle: "Interval Timer App for iPhone: What to Test First"
description: "On iPhone, the silent switch, Focus modes and the lock screen decide whether a timer cue fires on time. Five tests to run on any timer, Peak Interval included."
date: "2026-10-28"
featured_image: "/assets/blog/interval-timer-iphone.png"
image_alt: "A green iPhone lying face-down on a rubber gym floor beside a hex dumbbell, with a person squatting a barbell in soft window light behind it"
layout: "post.liquid"
tags: "posts"
category: "App Features"
---

You download an interval timer, build a 40/20 circuit, lock the iPhone and set it face-down by the dumbbells. Round three, the cue never comes. You pick the phone up and the clock is still running, perfectly on time. You just never heard it.

That is almost never the timer's maths. On iPhone, a cue that goes missing is usually the ring switch, a Focus mode, the way the app hands audio to iOS, or an app that only really works while it is open on screen. None of that shows up in an App Store listing. Ten minutes of testing on your own phone does show it.

## Test 1: flip the silent switch and lock the screen

Start a short workout, six rounds of 20/10 is plenty, then switch the phone to silent (the ring switch on older iPhones, the Action button or Control Centre on newer ones) and press the side button to lock it.

iOS sorts app audio into categories, and the category decides whether silent mode mutes it. A timer that plays its cues as **media audio**, the same way a music app does, keeps sounding with the ringer off. A timer that plays them as ambient sound, or fires them as **notification sounds**, goes quiet the moment you flip that switch. Most people train with their phone on silent, which is why this is the most common "my timer stopped beeping" complaint on iPhone.

Pass condition: every work, rest and final cue sounds on time, with the phone silenced and locked, without you touching it.

## Test 2: run it under your gym Focus

Focus modes are the second quiet killer. If you have a Fitness or Do Not Disturb Focus that switches on automatically at the gym, any timer that delivers cues through notifications will be muted by it, unless the app is on that Focus's allowed list.

Turn on the Focus you actually train with and repeat test 1. If cues disappear, either the app relies on notifications for timing, or you need to add it under **Settings → Focus → [your Focus] → Apps**. A timer that plays cues as audio from a running session is not affected by Focus at all, which is the behaviour you want. It is also worth running once with **Low Power Mode** on, since that is the state your phone is in at the end of a long day.

## Test 3: start Apple Music or Spotify first

Start a loud track, then start the timer. Listen for two things: can you hear each cue over the music, and does the music come back afterwards?

The good behaviour is **ducking**: iOS lowers your music for the length of the cue, then raises it again. A timer that takes over the audio session instead will pause your music at the first transition, and some apps never hand it back, so you finish the round in silence. A timer that mixes in without ducking plays a short beep at the same level as a dense track, and that is how cues get lost. We covered cue choice and volume in more detail in [interval timer with music](/blog/posts/interval-timer-with-music).

While you are here, check AirPods or other Bluetooth earbuds. Cues should route to them with the music, not out of the phone speaker on the floor.

## Test 4: look at the lock screen, not the app

A timer that is built for iPhone shows the workout on the lock screen and in the Dynamic Island as a **Live Activity**: the current phase, the countdown and the round, readable at a glance without unlocking. If nothing appears there while a session runs, you will be unlocking with sweaty hands to check how long is left, which is exactly what a timer is meant to save you.

Live Activities can be switched off per app, so if one is missing, check **Settings → [the timer] → Live Activities** before ruling the app out. In Peak Interval the lock-screen Live Activity also carries the skip control, so ending a set early is one tap through the glass while the phone stays propped against a plate.

## Test 5: the interruptions you will actually get

Real sessions get interrupted. During a rest phase, take or decline a call. Switch to your music app to skip a track and come back. Pause from the lock screen or your Watch, wait thirty seconds, resume.

A phone call is the hard one, because iOS takes the audio session away from every app while you are on the call. What you are checking is that the timer gets its cues back afterwards, and that pause and resume keep the phase and round you were on instead of jumping forward to catch up with the wall clock. If you train with an Apple Watch, run one round wrist-only too. Peak Interval's Watch app gives a haptic tap at the end of each rest and lets you pause or step back a phase from your wrist, and our [Apple Watch interval timer without your phone](/blog/posts/apple-watch-interval-timer-without-phone) guide covers what that setup can and cannot do.

## What this means for picking a timer on iPhone

Run these five tests on whatever you are considering, Peak Interval included, before you commit a programme to it. The two that catch most apps are the silent switch and your Focus, because they reflect how you actually train rather than how a review was written.

If a timer passes those two and shows the session on the lock screen, everything else is taste. On Android the failure points are different (battery managers and background services), which we walk through in the [Android version of this checklist](/blog/posts/interval-timer-app-android). If you need cues with no sound at all, the [silent interval timer](/blog/posts/silent-interval-timer-vibration-only) setup runs a whole session on haptics.
