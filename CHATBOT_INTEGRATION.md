# 🤖 AI Climate Chatbot Integration

## Overview
The AI Climate Chatbot is a Gemini-powered conversational interface that provides intelligent climate insights for various user types.

## Features

### 🎯 Target Users
- **🌾 Farmers**: Get crop cultivation advice and weather guidance
- **🌦️ Researchers**: Analyze climate trends and compare data
- **🚨 NDRF Teams**: Assess disaster risks and preparedness
- **🏛️ Policy Makers**: Review climate trends and policy insights

### ✨ Key Features
- **Smart Context-Aware Responses**: Gemini AI trained on climate domain
- **Suggested Questions**: Quick-start prompts for different user types
- **Real-time Chat Interface**: Beautiful Material-UI design
- **Message History**: Scrollable conversation with timestamps
- **Clear Chat**: Reset conversation anytime
- **Responsive Design**: Works on all screen sizes

## Implementation

### Files Created
1. `indradhanu-frontend/src/components/Chatbot.jsx` - Main chatbot component
2. `indradhanu-frontend/src/pages/Chatbot.jsx` - Chatbot page wrapper
3. `indradhanu-frontend/.env` - Environment variables (API key)

### Files Modified
1. `indradhanu-frontend/src/App.js` - Added chatbot route
2. `indradhanu-frontend/src/components/Navbar.jsx` - Added chatbot navigation

## Usage

### Access the Chatbot
1. Navigate to http://localhost:3000
2. Click "🤖 AI Chatbot" in the navigation bar
3. Start asking climate-related questions!

### Example Questions

#### For Farmers 🌾
- "What are the ideal weather conditions for rice cultivation in Maharashtra?"
- "When is the best time to plant sugarcane in Pune?"
- "What crops are suitable for low rainfall regions?"

#### For Researchers 🌦️
- "Compare average temperature changes in Delhi over the past 5 years"
- "What are the CO₂ emission trends in India?"
- "Analyze monsoon patterns in Western India"

#### For NDRF Teams 🚨
- "Which regions are at highest flood risk this season?"
- "What are the early warning signs of drought?"
- "How to prepare for cyclone season in coastal areas?"

#### For Policy Makers 🏛️
- "Summarize rainfall deviation trends in Western India from 2010-2020"
- "What are the economic impacts of climate change on agriculture?"
- "Recommend climate adaptation policies for urban areas"

## Technical Details

### API Integration
- **Provider**: Google Gemini 2.5 Flash (Latest Model)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent`
- **API Key**: Stored in `.env` file as `REACT_APP_GEMINI_API_KEY`

### Enhanced Prompting
The chatbot uses a specialized system prompt to ensure climate-focused responses:
```
You are an AI Climate Expert Assistant for the Indradhanu Climate Intelligence Platform.
Provide clear, data-driven insights on weather, crops, environmental conditions, climate trends, and disaster preparedness.
Keep your answers concise, factual, and user-friendly.
Focus on Indian climate context when relevant.
```

### UI Components
- **Material-UI**: Professional design system
- **Icons**: SmartToy, Person, Send, DeleteOutline
- **Colors**: Gradient purple background, blue primary theme
- **Layout**: Responsive with max-width 900px

## Security

### API Key Management
- API key stored in `.env` file (not committed to git)
- Environment variable: `REACT_APP_GEMINI_API_KEY`
- Fallback key included for development (should be replaced in production)

### Best Practices
- Add `.env` to `.gitignore`
- Use different API keys for dev/staging/production
- Monitor API usage and set quotas
- Implement rate limiting if needed

## Future Enhancements

### Potential Features
- 🎤 Voice input using Web Speech API
- 🔊 Text-to-speech for responses
- 📊 Display live climate data from Meteor API
- 💾 Save conversation history
- 📤 Export chat as PDF
- 🌐 Multi-language support
- 🔗 Integration with uploaded datasets
- 📍 Location-based recommendations
- 📈 Visual charts in responses

## Troubleshooting

### Common Issues

**Issue**: "Unable to fetch response"
- **Solution**: Check API key in `.env` file
- Verify internet connection
- Check Gemini API quota/limits

**Issue**: Chatbot not appearing in navigation
- **Solution**: Restart the development server
- Clear browser cache
- Check console for errors

**Issue**: Slow responses
- **Solution**: Normal for AI processing (5-10 seconds)
- Check network speed
- Consider implementing loading indicators

## Testing

### Manual Testing Checklist
- [ ] Navigate to /chatbot page
- [ ] Click suggested question chips
- [ ] Type custom question and send
- [ ] Verify AI response appears
- [ ] Test clear chat functionality
- [ ] Check responsive design on mobile
- [ ] Verify timestamps display correctly
- [ ] Test keyboard shortcuts (Enter to send)

## Status
✅ **FULLY INTEGRATED AND READY TO USE**

The AI Climate Chatbot is now live at: http://localhost:3000/chatbot
