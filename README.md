# Email Signature Tests

This repository contains tests to verify that the fish icon in the email signature loads properly.

## Files

- `clean_signature.html` - Email signature with base64-encoded fish icon
- `personal_signature.html` - Email signature with direct reference to fish.png
- `test_signature.js` - Playwright tests to verify image loading

## Setup

1. Install dependencies:

```bash
npm install
```

2. Install Playwright browsers:

```bash
npx playwright install chromium
```

## Running Tests

Run the tests with:

```bash
npm test
```

## Test Description

The tests verify that:

1. The base64-encoded fish icon in clean_signature.html loads properly
2. The direct reference to fish.png in personal_signature.html loads properly

## Troubleshooting

If the image doesn't load:

1. Check that the fish.png file exists in the root directory
2. Ensure the base64 encoding doesn't have line breaks
3. Verify the MIME type is correct (image/png)