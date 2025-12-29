# Troubleshooting: Assessment Error Fixes

## Issues Fixed

### 1. ✅ Better Error Handling
- Updated API client with interceptors for better error logging
- Improved error messages in UploadPage to show specific errors
- Added network error detection (server not running, timeout, etc.)

### 2. ✅ FormData Header Issue
- Removed manual `Content-Type` header setting - let axios handle it automatically
- This fixes multipart/form-data submission issues

### 3. ✅ Result Page Error Display
- Better error message display
- Added "Go to Dashboard" button for easier navigation
- Improved error card styling

### 4. ✅ Result Validation
- Added validation to ensure result has required fields
- Better handling of malformed responses

## Common Issues and Solutions

### Issue: "Cannot connect to the server"
**Solution:**
1. Make sure the backend is running: `cd backend && python main.py`
2. Check which port it's using (might be 8001, 8002, etc. if 8000 is busy)
3. Update `frontend/src/api/client.js` with the correct port:
   ```javascript
   baseURL: "http://127.0.0.1:8001", // Use the port from backend console
   ```

### Issue: "Request timeout"
**Solution:**
- The timeout is set to 60 seconds
- If your model inference takes longer, the image might be too large
- Try with a smaller image or check backend logs for errors

### Issue: "Assessment failed" or "Invalid assessment result"
**Solution:**
1. Check backend console for error messages
2. Verify model files are loaded correctly
3. Check that the image is a valid format (JPG, PNG)
4. Make sure the image shows a skin lesion

### Issue: Results page shows error but backend seems fine
**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Check Network tab to see the actual API response
4. Verify the response has `success: true` and required fields

## Testing Steps

1. **Start Backend:**
   ```bash
   cd backend
   python main.py
   ```
   Note the port number shown in console

2. **Update Frontend API Client** (if port is not 8000):
   Edit `frontend/src/api/client.js` and update `baseURL` to match backend port

3. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Test Upload:**
   - Go to Upload page
   - Select an image
   - Fill in optional fields
   - Click "Analyze Risk"
   - Check browser console for errors
   - Check backend console for processing logs

5. **Verify Results:**
   - Results page should show risk level, percentages, explanations
   - If error appears, check the error message for details

## Debugging Tips

- **Backend Console:** Shows detailed processing information
- **Browser Console (F12):** Shows frontend errors and API calls
- **Network Tab (F12):** Shows actual HTTP requests/responses
- **LocalStorage:** Check browser DevTools > Application > LocalStorage for stored results

## Expected Behavior

1. Upload image → Shows analyzing page
2. Backend processes → Console shows "✓ Assessment saved"
3. Results page loads → Shows risk level, breakdown, explanations
4. Dashboard updates → Shows latest assessment

If any step fails, check the error message for specific guidance!

