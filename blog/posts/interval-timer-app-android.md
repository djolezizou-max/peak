---
title: "Interval Timer App for Android: What to Test Before You Trust One Mid-Workout"
seoTitle: "Interval Timer App for Android: What to Test First"
description: "On Android, battery saver, a locked screen and your music app decide if a timer cue fires on time. Five tests to run on any interval timer, Peak Interval too."
date: "2026-10-18"
featured_image: "/assets/blog/interval-timer-app-android.png"
image_alt: "Water bottle, red resistance band and a phone lying on a rubber gym floor in warm window light, with a person's trainers mid-jump behind them"
layout: "post.liquid"
tags: "posts"
category: "Buying Guides"
---

You pick an interval timer from the Play Store, build a 40/20 circuit, lock the phone and drop it on the floor. Round three, the cue never comes. You pick the phone up and the timer is frozen at 0:17, or it is still counting but the beep went missing somewhere underneath your playlist.

That is rarely the timer's maths being wrong. On Android, whether a cue fires at second 40 depends on how the app runs in the background, how your phone's manufacturer handles battery, and how the app shares audio with everything else. Feature lists do not tell you any of that. Ten minutes of testing does.

## Test 1: lock the screen and walk away

The first thing to check is the simplest. Start a short workout — six rounds of 20/10 is enough — press the power button, and put the phone face-down. Do not touch it until the timer should have finished.

A timer built properly for Android runs as a **foreground service**: it shows a persistent notification while the workout is active, and the system treats it like music playback rather than an app you have walked away from. If you see no notification at all while a workout runs, that is a warning sign. It usually means the app is relying on staying open on screen, and the first time the display sleeps, its clock goes with it.

Pass condition: every transition sounds on time with the screen off, and the final cue fires when the six rounds end, not when you next pick the phone up.

## Test 2: run it with battery saver on

Android lets each manufacturer add its own battery management on top of the stock system, and some of them are aggressive. Samsung, Xiaomi, OnePlus, Huawei and Oppo phones are the ones people most often report killing apps mid-session. A timer that passes test 1 on a Pixel can fail it on a Galaxy with battery saver enabled.

So run test 1 again with battery saver switched on, since that is the state your phone is in at the end of a long day. If it fails, open **Settings → Apps → [the timer] → Battery** and set it to **Unrestricted** (some phones call it "Don't optimise" or put it under "Background usage limits"). That exemption is the single setting that fixes most "the timer stopped" complaints.

If a timer only survives with every restriction removed and the screen kept on, it is not a timer you can trust with a 45-minute session.

## Test 3: start your music first

Open Spotify or YouTube Music, start a loud track, then start the timer. Listen for two things: whether the cue is audible over the music, and whether the music recovers afterwards.

The behaviour you want is **ducking** — the music drops in volume for the length of the cue and comes straight back. Apps that grab full audio focus pause your music at every transition instead, and some streaming apps do not resume reliably, so you finish a round to silence. Apps that do neither just play a short beep at the same level as a dense mix, which is how cues go missing. We went through this in more detail, including cue choice and speaker setup, in [interval timer with music](/blog/posts/interval-timer-with-music).

Pass condition: you hear both the work and rest cue with your eyes closed, at your normal music volume.

## Test 4: earbuds, Do Not Disturb and media volume

Two Android quirks catch people out. First, many timers play cues on the **media** volume, not the ringer or alarm volume, so a phone on silent can still beep — and a phone with media turned down will not, however loud the ringer is. Check which slider the app actually uses before deciding the timer is broken.

Second, connect your Bluetooth earbuds and confirm the cues route to them, then turn on Do Not Disturb and run a round. A timer that plays cues as notification sounds will go quiet under Do Not Disturb, which is exactly the mode many people use in the gym.

## Test 5: the interruptions you will actually get

Real sessions get interrupted. Mid-workout, pull down the notification shade and pause from there, then resume. Answer or decline a call during a rest phase. Switch to your music app to skip a track and come back.

What you are checking is that pause and resume keep the phase and round you were on, and that the clock continues from where it stopped rather than snapping forward to catch up with wall time. Controls in the persistent notification matter more than they sound — with chalky or sweaty hands, unlocking the phone to press pause is a step you will skip.

## What this means for picking a timer

Run all five tests on whichever app you are considering, on your own phone, before you commit a programme to it. It is the only way to account for your manufacturer's battery rules, and it takes less time than one ruined session.

Peak Interval is on [Android](https://play.google.com/store/apps/details?id=com.roli.intervals) as well as iPhone, and it is worth putting through exactly these tests. What matters on any platform is the same: separate sounds for work, rest and preparation so the cue tells you which phase you are in, a preparation phase long enough to get the phone down and start your music, and saved workouts so tomorrow's session is one tap rather than a rebuild. If the timer passes the lock-screen and battery-saver tests on your phone, everything else is a matter of taste.
