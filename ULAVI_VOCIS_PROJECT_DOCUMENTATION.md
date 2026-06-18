# ULAVI VOCIS 3.0 Project Documentation

## 1. Project Overview

ULAVI VOCIS is an AI-powered multilingual travel concierge web application. It allows customers to speak or type naturally, detects their language, collects travel booking details step by step, validates the information, shows a review page, and submits a lead to operations.

The project was rebuilt from a single-file prototype into a structured full-stack application with:

- React + Vite frontend
- Express backend
- Voice recording and transcription
- Multilingual conversation flow
- Travel entity extraction
- Booking progress tracking
- Review and confirmation flow
- Supabase lead storage
- SendGrid email notifications
- Twilio WhatsApp notifications

## 2. Product Goal

The application is designed for both educated and non-technical users. It should be simple enough for older users and uneducated customers to understand:

1. Choose a travel service.
2. Speak naturally.
3. Answer simple questions.
4. Review collected details.
5. Confirm the request.
6. Receive a reference number.

The main product principle is:

> Home page should be simple and trustworthy. Chat page should convert. Review page should confirm. Success page should reassure.

## 3. Core Services

ULAVI VOCIS supports these service types:

- Airport Transfer
- Ground Transfer
- Long Distance Transfer
- Cross Border Transfer
- Day / Hourly Packages
- Tour Packages
- Medical Equipment Transfer

Each service has a different required-field set.

## 4. User Journey

### Home Page

Purpose:

- Introduce ULAVI VOCIS.
- Show the main voice-first microphone hero.
- Let users start a conversation.
- Let users choose a service directly.
- Let returning users track a request.

Current design direction:

- White background
- Navy + gold palette
- Large serif headline
- Voice-first microphone section
- Premium service cards
- Track Request card
- Minimal animations
- Large spacing

### Chat Page

Purpose:

- Collect booking details conversationally.
- Support voice and text input.
- Show booking progress.
- Detect language dynamically.
- Allow service and language selection.
- Allow users to listen to AI replies.

Important chat features:

- Large microphone button
- Linear voice waveform
- Voice Responses ON/OFF toggle
- Listen/Stop button under assistant messages
- Language selector
- More languages menu
- Service selector
- Booking Progress card
- Dynamic missing-field logic

### Review Page

Purpose:

- Show all collected details before submission.
- Let user verify travel, passenger, and contact details.
- Allow edit before submit.
- Submit only after user confirms.

### Success Page

Purpose:

- Show request submitted confirmation.
- Show reference number.
- Allow copying reference.
- Allow downloading summary.
- Offer support options.
- Let user create another request or return home.

## 5. Technology Stack

### Frontend

- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Lucide React icons

### Backend

- Node.js
- Express
- Zod
- Helmet
- CORS
- dotenv

### External Services

- OpenAI for voice transcription and optional intelligence
- Supabase for database storage
- SendGrid for email
- Twilio for WhatsApp

## 6. Project Structure

```text
C:\voiceB
├── backend
│   ├── controllers
│   │   ├── conversationController.js
│   │   └── leadController.js
│   ├── middleware
│   │   └── errorHandler.js
│   ├── routes
│   │   ├── conversationRoutes.js
│   │   └── leadRoutes.js
│   ├── services
│   │   ├── AirportResolver.js
│   │   ├── BookingEntityExtractor.js
│   │   ├── BookingProgressService.js
│   │   ├── ConversationMemoryManager.js
│   │   ├── DateTimeNormalizer.js
│   │   ├── EmailNormalizer.js
│   │   ├── LanguageDetectionService.js
│   │   ├── LocationAliasDictionary.js
│   │   ├── LocationResolver.js
│   │   ├── PhoneNormalizer.js
│   │   ├── PhoneValidationRules.js
│   │   ├── TranscriptionCorrectionDictionary.js
│   │   ├── TravelEntityDictionary.js
│   │   ├── TravelEntityExtractor.js
│   │   ├── TravelIntentDetector.js
│   │   ├── TravelIntentPatterns.js
│   │   ├── TravelLanguageDataset.js
│   │   ├── conversationService.js
│   │   ├── languageUnderstanding.js
│   │   ├── leadService.js
│   │   ├── notificationService.js
│   │   ├── openaiService.js
│   │   └── supabaseService.js
│   └── server.js
├── database
│   └── schema.sql
├── docs
│   └── architecture.md
├── src
│   ├── components
│   │   ├── AppRail.jsx
│   │   ├── BrandMark.jsx
│   │   ├── ChatMessage.jsx
│   │   ├── ReadyModal.jsx
│   │   ├── ServiceCard.jsx
│   │   ├── SubmissionCelebration.jsx
│   │   ├── SummaryPanel.jsx
│   │   ├── Toast.jsx
│   │   └── VoiceRecorder.jsx
│   ├── pages
│   │   ├── Chat.jsx
│   │   ├── Home.jsx
│   │   ├── Review.jsx
│   │   └── Success.jsx
│   ├── services
│   │   ├── api.js
│   │   └── serviceCatalog.js
│   ├── styles
│   │   └── index.css
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

## 7. Frontend Architecture

### Main State Owner

`src/App.jsx` controls:

- Current screen
- Conversation messages
- Draft booking details
- Missing fields
- Required fields
- Booking progress
- Ready modal state
- Success result
- Toast messages

Main screens:

- `home`
- `chat`
- `review`
- `success`

### Important Frontend Components

#### `VoiceRecorder.jsx`

Handles:

- Browser microphone access
- MediaRecorder
- Audio chunk collection
- Audio base64 conversion
- Minimum recording duration
- Mic visual state
- Linear waveform animation
- Voice quality score

Recent fixes:

- Prevents empty `audioBase64` submissions.
- Avoids false “too short” errors for valid 3-5 second recordings.
- Uses reliable timing with `performance.now()`.
- Calls `requestData()` before stop to flush audio chunks.
- Waveform height reacts to actual voice energy.

#### `ChatMessage.jsx`

Handles:

- User and assistant chat bubbles
- Message timestamps
- Language badge
- Listen/Stop button for assistant messages
- Browser SpeechSynthesis TTS

Voice output rules:

- Assistant messages only.
- No automatic speaking.
- User chooses Listen manually.
- Voice Responses ON/OFF controls visibility.

#### `SummaryPanel.jsx`

Shows:

- Selected service
- Progress percentage
- Filled/required details count
- Next missing field
- Review Details button

#### `ReadyModal.jsx`

Appears when all required details are collected.

Allows:

- Review and submit
- Continue editing
- Voice confirmation

#### `SubmissionCelebration.jsx`

Temporary popup after successful submission.

Current design:

- Glass-style popup
- Enhanced navy/black readable text
- Success check icon
- Animated decorative particles

#### `Toast.jsx`

Shows short status messages:

- Success
- Error
- Voice retry messages

## 8. Backend Architecture

### Server

`backend/server.js`

Responsibilities:

- Load environment variables.
- Configure Express.
- Enable CORS.
- Enable Helmet.
- Parse JSON up to 16 MB.
- Serve API routes.
- Serve production frontend from `dist`.

Default backend URL:

```text
http://127.0.0.1:3000
```

### API Routes

#### Health

```http
GET /api/health
```

Returns enabled service status:

- OpenAI
- Supabase
- SendGrid
- Twilio

#### Text Conversation

```http
POST /api/conversation/message
```

Payload:

```json
{
  "message": "I need airport pickup from Chennai Airport",
  "draft": {},
  "messages": []
}
```

Returns:

```json
{
  "language": "English",
  "draft": {},
  "requiredFields": [],
  "missingFields": [],
  "progress": {},
  "readyForReview": false,
  "reply": "Great, where should the pickup be?"
}
```

#### Voice Conversation

```http
POST /api/conversation/voice
```

Payload:

```json
{
  "audioBase64": "...",
  "mimeType": "audio/webm",
  "draft": {},
  "messages": []
}
```

Voice endpoint behavior:

- Rejects empty audio with clean `400`.
- Transcribes audio using OpenAI when configured.
- If transcription fails, returns a friendly retry message instead of crashing.

#### Lead Submission

```http
POST /api/leads
```

Payload:

```json
{
  "draft": {},
  "messages": []
}
```

Creates:

- Supabase lead
- Supabase message transcript rows
- Email notification
- WhatsApp notification
- Operations notification

#### Track Lead

```http
GET /api/leads/:reference
```

Returns lead status for tracking.

## 9. Conversation Flow

The conversation engine lives in:

```text
backend/services/conversationService.js
```

Flow:

1. User sends text or voice transcript.
2. Backend detects language.
3. Backend detects service type.
4. Backend extracts travel entities.
5. Backend merges valid new entities into draft.
6. Backend validates fields.
7. Backend calculates missing fields.
8. Backend replies with the next question.
9. When all fields are filled, `readyForReview` becomes true.

Important rule:

> Ask only one missing detail at a time.

## 10. Required Fields by Service

### Airport Transfer

- Service Type
- Pickup
- Dropoff
- Date
- Time
- Passengers
- Name
- Phone
- Email

### Ground Transfer

- Service Type
- Pickup
- Dropoff
- Date
- Time
- Passengers
- Name
- Phone
- Email

### Long Distance Transfer

- Service Type
- Pickup
- Dropoff
- Date
- Time
- Passengers
- Name
- Phone
- Email

### Cross Border Transfer

- Service Type
- Pickup
- Dropoff
- Date
- Time
- Passengers
- Name
- Phone
- Email

### Day / Hourly Packages

- Service Type
- Pickup
- Dropoff
- Date
- Time
- Passengers
- Package Hours
- Name
- Phone
- Email

### Tour Packages

- Service Type
- Pickup
- Dropoff
- Date
- Passengers
- Name
- Phone
- Email

### Medical Equipment Transfer

- Service Type
- Pickup
- Dropoff
- Date
- Time
- Equipment
- Name
- Phone
- Email

## 11. Language Support

Supported languages and styles:

- English
- Tamil
- Tanglish
- Hindi
- Malayalam
- Kannada
- Telugu
- Bengali
- Urdu
- Arabic
- Malay
- French
- Chinese
- Japanese
- Korean
- Vietnamese

Language rules:

- English input should get English output.
- Tamil input should get Tamil output.
- Tanglish input should get Tanglish output.
- French input should get French output.
- Hindi input should get Hindi output.
- Language should update dynamically based on recent user speech.

## 12. Voice System

### Voice Input

Frontend:

```text
src/components/VoiceRecorder.jsx
```

Backend:

```text
backend/services/openaiService.js
backend/services/conversationService.js
```

Voice process:

1. User taps mic.
2. Browser asks for microphone permission.
3. MediaRecorder records audio.
4. Audio chunks are converted to Base64.
5. Frontend sends `audioBase64` to backend.
6. Backend transcribes audio.
7. Transcript is processed like text input.

### Voice Output

Frontend:

```text
src/components/ChatMessage.jsx
```

Rules:

- No auto-speaking.
- Assistant messages show Listen.
- User can stop speaking.
- Voice Responses toggle can hide/show Listen buttons.
- Preference is stored in localStorage.

LocalStorage key:

```text
ulavi_voice_responses_enabled
```

## 13. Entity Extraction

Main files:

```text
backend/services/BookingEntityExtractor.js
backend/services/TravelEntityExtractor.js
backend/services/languageUnderstanding.js
backend/services/ConversationMemoryManager.js
```

Extracted fields:

- Service Type
- Pickup Location
- Dropoff Location
- Date
- Time
- Passenger Count
- Customer Name
- Mobile Number
- Email
- Equipment
- Package Hours
- Notes

Examples:

```text
coimbatore poganum -> Coimbatore
villivakkam varaikum -> Villivakkam
morning ten o clock -> 10:00 AM
motham pathu peru -> 10 passengers
7824-8492-54 -> 7824849254
```

## 14. Dynamic Update Commands

Users can update collected details naturally.

Examples:

```text
Update the dropoff location to Villivakkam.
Change the contact name to Bharathi.
Remove the phone number.
Pickup location badhilaga Chennai Airport.
Name maathu Sivaraman.
```

Supported update words include:

- update
- change
- correct
- replace
- remove
- clear
- maatru
- maathu
- badhilaga
- badlo
- sahi karo
- changer
- remplacer

## 15. Phone Validation

Main file:

```text
backend/services/PhoneValidationRules.js
```

Important production rule:

> Customer WhatsApp number is not always from the travel country.

So an Indian number like:

```text
7824849254
```

must be accepted even when the journey is in Singapore, Malaysia, UAE, or another country.

### India Rule

Accepted:

```text
7824849254
7824-8492-54
+91 7824849254
917824849254
seven eight two four eight four nine two five four
seven eight two four, eighty four, ninety two, fifty four
```

Rejected:

```text
1234567890
2345678901
3456789012
5678901234
```

India regex:

```regex
^[6-9][0-9]{9}$
```

### Supported Phone Countries

- India
- Singapore
- Malaysia
- UAE
- Saudi Arabia
- France
- Japan
- China
- Vietnam
- Indonesia
- Thailand
- South Korea
- UK
- USA
- Australia

## 16. Data Normalization

Normalization files:

```text
backend/services/DateTimeNormalizer.js
backend/services/EmailNormalizer.js
backend/services/PhoneNormalizer.js
backend/services/LocationResolver.js
backend/services/LocationAliasDictionary.js
backend/services/TranscriptionCorrectionDictionary.js
```

Data rules:

- Do not store conversational filler.
- Do not store raw transcript as pickup/dropoff.
- Normalize locations to clean names.
- Normalize phone to digits.
- Normalize date to ISO when possible.
- Normalize time to `HH:MM AM/PM`.

## 17. Database

Supabase schema file:

```text
database/schema.sql
```

Tables:

### `public.leads`

Fields:

- `id`
- `reference_number`
- `service_type`
- `name`
- `email`
- `phone`
- `language`
- `summary`
- `status`
- `metadata`
- `created_at`

### `public.messages`

Fields:

- `id`
- `lead_id`
- `role`
- `message`
- `created_at`

Indexes:

- `leads_status_created_at_idx`
- `leads_service_type_idx`
- `messages_lead_id_created_at_idx`

## 18. Supabase Setup

For a fresh Supabase project:

1. Open Supabase dashboard.
2. Open SQL Editor.
3. Paste and run:

```text
database/schema.sql
```

4. Add environment variables.
5. Restart backend.

If you see:

```text
Could not find the table 'public.leads' in the schema cache
```

Run `database/schema.sql` in Supabase SQL Editor and restart backend.

## 19. Environment Variables

Create `.env` from `.env.example`.

Use placeholders like this:

```env
PORT=3000
NODE_ENV=development
APP_BASE_URL=http://127.0.0.1:5173
FRONTEND_DIST=dist

OPENAI_API_KEY=your_openai_key
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TRANSCRIBE_MODEL=gpt-4o-mini-transcribe

SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_supabase_publishable_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=your_verified_sender_email
OPERATIONS_EMAIL=operations_email

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_PHONE_NUMBER=your_twilio_phone_number

OPERATIONS_WHATSAPP=whatsapp:+countrycode_number
```

Security note:

- Do not commit real keys.
- Do not expose service-role keys in frontend.
- Rotate any key that was accidentally committed.

## 20. Notification System

Main file:

```text
backend/services/notificationService.js
```

Notifications:

- Customer email confirmation
- Customer WhatsApp confirmation
- Operations email alert
- Operations WhatsApp alert
- Conversation transcript summary

Providers:

- SendGrid
- Twilio WhatsApp

If provider keys are missing:

- Lead flow still works in demo mode.
- Notifications are skipped or reported as unavailable.

## 21. Lead Submission Flow

Main files:

```text
backend/controllers/leadController.js
backend/services/leadService.js
backend/services/notificationService.js
```

Flow:

1. Frontend calls `POST /api/leads`.
2. Backend creates reference number.
3. Backend stores lead in Supabase.
4. Backend stores conversation messages.
5. Backend sends notifications.
6. Backend returns success result.
7. Frontend shows success page.

## 22. Request Tracking

Home page contains Track Request card.

User enters:

```text
ULV-XXXXXXXX
```

Frontend calls:

```http
GET /api/leads/:reference
```

Tracking displays:

- Reference
- Service
- Current status
- Timeline state

## 23. Important UI Decisions

### Home Page

Current direction:

- Simple white premium layout.
- Big mic hero.
- No car box.
- No globe box.
- No heavy background image.
- Clear services.
- Bottom Track Request card.
- Header uses `24/7 Travel Help` instead of duplicate Track Request.

### Chat Page

Current direction:

- 80% conversation area.
- 20% booking progress area.
- Voice-first mic section.
- Linear waveform.
- Language chooser under mic.
- Service chooser hides other services after service selection.
- Voice Responses toggle in top-right of mic hero.

### Review Page

Current direction:

- White + light gray + navy.
- Clean sections.
- No extra trust strip.
- Clear Submit Request button.

### Success Page

Current direction:

- White background.
- Components placed toward top.
- Reference number central.
- Need Help and estimated response time.

## 24. Run Locally

Install:

```bash
npm install
```

Run frontend and backend:

```bash
npm run dev
```

Run only frontend:

```bash
npm run dev:frontend
```

Run only backend:

```bash
npm run dev:backend
```

Frontend:

```text
http://127.0.0.1:5173
```

Backend:

```text
http://127.0.0.1:3000
```

Build:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

Start production server:

```bash
npm start
```

## 25. Common Errors and Fixes

### Port 3000 Already In Use

Error:

```text
EADDRINUSE: address already in use :::3000
```

Fix:

- Stop existing Node backend.
- Or run with another port.

Example:

```bash
PORT=3001 npm run dev:backend
```

### Supabase Table Missing

Error:

```text
Could not find the table 'public.leads' in the schema cache
```

Fix:

- Run `database/schema.sql` in Supabase SQL Editor.
- Restart backend.

### Voice API 500

Cause:

- OpenAI transcription missing/failing.
- Empty audio payload.

Fixes already added:

- Empty audio returns clean 400.
- Transcription failure returns retry message instead of crashing.
- Frontend blocks empty recordings.

### Recording Too Short

Cause:

- Previously used blob size check.

Fix:

- Removed fragile blob size validation.
- Duration uses `performance.now()`.
- Recorder flushes chunks with `requestData()` before stop.

## 26. Testing Checklist

### Build

```bash
npm run build
```

### Backend Import Check

```bash
node --input-type=module -e "import('./backend/services/conversationService.js').then(() => console.log('ok'))"
```

### Health Check

```bash
curl http://127.0.0.1:3000/api/health
```

### Phone Test Cases

Must pass:

```text
7824849254
7824-8492-54
+91 7824849254
917824849254
seven eight two four eight four nine two five four
seven eight two four, eighty four, ninety two, fifty four
```

Conversation should move to:

```text
Which email should receive the confirmation?
```

## 27. Documentation Files

Existing project docs:

- `README.md`
- `docs/architecture.md`
- `PRODUCTION_AUDIT.md`
- `PHONE_VALIDATION_AUDIT.md`
- `MULTILINGUAL_TEST_CASES.md`
- `VALIDATION_RULES.md`
- `LOCATION_NORMALIZATION_DATASET.json`
- `TRAVEL_PHRASES_DATASET.json`
- `SLANG_DATASET.json`

This file:

```text
ULAVI_VOCIS_PROJECT_DOCUMENTATION.md
```

is the complete consolidated project documentation.

## 28. Production Readiness Notes

Before production:

- Use a real Supabase service role key only on backend.
- Rotate any exposed API keys.
- Replace broad Supabase anon policies with safer scoped access.
- Verify SendGrid sender identity.
- Verify Twilio WhatsApp sandbox or production sender.
- Add automated tests for extraction and phone validation.
- Add monitoring for failed notifications.
- Add operations dashboard for lead review.

## 29. Ownership Summary

ULAVI VOCIS is a voice-first AI travel concierge. The core value is not only the UI, but the full booking pipeline:

- Natural multilingual speech
- Clean structured extraction
- Human-friendly booking conversation
- Dynamic progress tracking
- Review-before-submit safety
- Operations-ready lead generation
- Email and WhatsApp confirmation

The heart of the product is the chat mic and booking extraction flow. UI changes should not break:

- Voice recording
- Transcription
- Draft state
- Missing-field logic
- Phone validation
- Review confirmation
- Lead submission
