# Base44 Prompt: VS Health Benefits Member App

Copy everything below the line into Base44.

---

Build a mobile-first member app for **VS Health Benefits**, a licensed independent health insurance brokerage. The app is the member/client portal, designed to run as an iOS and Android app. It should feel modern, clean, and trustworthy, like a fintech app.

## Brand and style
- Company name: VS Health Benefits. Logo mark: a rounded square with the letters "VS" in white on a blue-to-teal gradient.
- Colors: deep navy #0b2346, primary blue #16447f and #1e5ab0, accent teal #0db5a6, success green #0a8754, light background #f7faff, white cards.
- Fonts: Poppins for headings, Inter for body text.
- Rounded cards, soft shadows, pill-shaped buttons, a dark navy sidebar/nav. Mobile-first with a bottom tab bar on phones.
- No em dashes anywhere in the copy.

## Users and roles
1. **Member (client)**: signs up and logs in to manage their info, submit referrals, track rewards, view their plan, and message support.
2. **Admin (staff)**: sees all members and referrals, can mark a referral as "sold", update payout status, message members, and view their plan details. Admin is a protected role.

Use email and password authentication with signup, login, and password reset.

## Main member screens (bottom tab bar / sidebar)

### 1. Dashboard (home)
- Personalized greeting ("Welcome back, [First name]").
- Summary cards: total referrals submitted, referrals sold, total rewards earned, rewards pending.
- A "Getting started" checklist for new users (complete profile, submit first referral, etc.).
- A primary "Refer someone and earn" button that opens the Send Referral flow.
- Recent activity list (latest referrals and their status).

### 2. Send Referral (multi-step wizard)
A friendly step-by-step form to refer a friend or family member:
- Step 1: Who are you referring (referral first name, last name).
- Step 2: Contact info (phone, email).
- Step 3: What they need (coverage type: individual health, family health, dental and vision, Medicare, self-employed/1099, small business).
- Step 4: Review and submit.
On submit: save the referral, show a celebratory confirmation with a confetti animation, and notify the admin. Each referral starts with status "submitted".

### 3. My Referrals
- A list of all referrals the member has submitted, each showing the referred person's name, coverage type, date, current status, and reward amount.
- Status pipeline: Submitted, Contacted, In Progress, Sold, Paid.
- When a referral is marked "Sold" by admin, the member sees a celebration (confetti) and a "Your referral sold!" message. When it moves to "Paid", show a "Payment on the way!" message.
- Show a running total of earned and pending rewards.

### 4. My Plan
- Shows the member's current health insurance plan details: carrier, plan name, coverage tier (Bronze/Silver/Gold/etc.), monthly premium, effective date, member ID, and coverage type.
- If no plan is on file yet, show a friendly empty state with a "Get a free quote" button.

### 5. Support
- A simple two-way message thread between the member and the VS Health Benefits support team.
- Members can send messages; admin replies appear in the thread.
- Unread messages show a badge on the Support tab.
- Push notification when support replies.

### 6. Settings / Profile
- Editable profile: first name, last name, email, phone, date of birth, address, city, state, ZIP.
- Notification preferences toggle.
- A unique referral link the member can copy and share.
- Log out.

## Admin screens
- **Members list**: searchable list of all members with contact info and plan status. Tap to view a member, edit their profile, and see their plan and referrals.
- **Referrals board**: all referrals across all members in a pipeline (Submitted, Contacted, In Progress, Sold, Paid). Admin can move a referral through stages and set the reward/payout amount. Marking "Sold" and "Paid" triggers the member celebrations and notifications.
- **Messages**: inbox of member support threads; admin can reply.
- **Dashboard**: totals for members, open referrals, referrals sold this month, and rewards paid.

## Data models
- **User/Member**: firstName, lastName, email, phone, dateOfBirth, address, city, state, zip, role (member/admin), referralCode, createdAt, lastActive.
- **Referral**: referredById (the member), referralFirstName, referralLastName, referralPhone, referralEmail, coverageType, status (submitted/contacted/in_progress/sold/paid), rewardAmount, notes, createdAt.
- **Plan**: memberId, carrier, planName, tier, monthlyPremium, effectiveDate, memberIdNumber, coverageType.
- **Message**: memberId, from (member/admin), body, read, createdAt.
- **Notification**: userId, title, body, type, read, createdAt.

## Key behaviors
- Real-time sync so admin actions (marking a referral sold, replying to a message) show up for the member right away.
- Celebration/confetti moments when a referral is submitted, sold, and paid, to make the Refer and Earn program feel rewarding.
- Push notifications for: referral status changes, support replies, and reward payouts.
- Mobile-first, works great on phones, and installable as an iOS and Android app.
- A friendly first-login welcome and a short guided tour of the tabs for brand-new members.

## Tone of copy
Warm, encouraging, and simple. This is a Refer and Earn rewards app on top of a member portal, so the experience should make members feel appreciated and make referring easy and fun.
