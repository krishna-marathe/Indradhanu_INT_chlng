# 🌬️ Air Quality Index (AQI) Integration

## Overview
Added comprehensive Air Quality Index (AQI) display to the Weather page, fetching real-time air quality data from the World Air Quality Index (WAQI) API.

## Features Implemented

### ✅ Backend API Endpoint
**New Route**: `GET /aqi/current`

#### Parameters
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate

#### Response Data
```json
{
  "message": "AQI data retrieved successfully",
  "data": {
    "aqi": 70,
    "category": "Moderate",
    "color": "#ffff00",
    "health_implications": "Air quality is acceptable...",
    "cautionary_statement": "Unusually sensitive people should...",
    "dominant_pollutant": "PM2.5",
    "pollutants": {
      "pm25": { "name": "PM2.5", "value": 70, "unit": "μg/m³" },
      "pm10": { "name": "PM10", "value": 27, "unit": "μg/m³" },
      "o3": { "name": "Ozone (O₃)", "value": 26.4, "unit": "ppb" },
      "no2": { "name": "Nitrogen Dioxide (NO₂)", "value": 24.7, "unit": "ppb" },
      "so2": { "name": "Sulfur Dioxide (SO₂)", "value": 4.1, "unit": "ppb" },
      "co": { "name": "Carbon Monoxide (CO)", "value": 6.4, "unit": "ppb" }
    },
    "location": {
      "city": "Mumbai",
      "latitude": 19.076,
      "longitude": 72.8777,
      "station_url": "..."
    },
    "last_update": "2025-11-07 17:00:00",
    "timestamp": "2025-11-07T17:30:00"
  }
}
```

### ✅ Frontend Component
**New Component**: `AQIDisplay.jsx`

#### Features
1. **Real-time AQI Display**
   - Large, color-coded AQI value
   - Category badge (Good, Moderate, Unhealthy, etc.)
   - Visual icon based on air quality level
   - Location and update time

2. **Health Information**
   - Health implications based on AQI level
   - Cautionary statements for sensitive groups
   - Color-coded alerts

3. **Pollutant Breakdown**
   - Individual pollutant values
   - PM2.5, PM10, O₃, NO₂, SO₂, CO
   - Units displayed (μg/m³ or ppb)
   - Dominant pollutant highlighted

4. **Visual Elements**
   - Progress bar showing AQI level (0-500 scale)
   - Color-coded cards for each pollutant
   - AQI scale reference guide
   - Responsive grid layout

5. **Interactive Features**
   - Tooltips on pollutant cards
   - Hover effects
   - Auto-refresh when location changes

## AQI Categories & Colors

| AQI Range | Category | Color | Health Impact |
|-----------|----------|-------|---------------|
| 0-50 | Good | 🟢 Green (#00e400) | Satisfactory, no risk |
| 51-100 | Moderate | 🟡 Yellow (#ffff00) | Acceptable for most |
| 101-150 | Unhealthy for Sensitive | 🟠 Orange (#ff7e00) | Sensitive groups affected |
| 151-200 | Unhealthy | 🔴 Red (#ff0000) | Everyone may be affected |
| 201-300 | Very Unhealthy | 🟣 Purple (#8f3f97) | Health alert |
| 301+ | Hazardous | 🔴 Maroon (#7e0023) | Emergency conditions |

## Data Source

### WAQI (World Air Quality Index) API
- **Website**: https://waqi.info/
- **API Endpoint**: `https://api.waqi.info/feed/geo:{lat};{lon}/`
- **Token**: Using demo token (limited to 1000 requests/day)
- **Coverage**: Global air quality monitoring stations
- **Update Frequency**: Hourly

### Pollutants Tracked
1. **PM2.5** - Fine particulate matter (< 2.5 micrometers)
2. **PM10** - Coarse particulate matter (< 10 micrometers)
3. **O₃** - Ground-level ozone
4. **NO₂** - Nitrogen dioxide
5. **SO₂** - Sulfur dioxide
6. **CO** - Carbon monoxide

## Integration in Weather Page

### Location
The AQI component is displayed on the Weather page (`/weather`) immediately after the location information and before the weather statistics.

### Auto-Update
The AQI data automatically updates when:
- User changes location
- User clicks "Fetch Data" or "Analyze"
- Coordinates are updated

### Error Handling
- Graceful fallback if AQI data unavailable
- Warning message displayed
- Doesn't block weather data display

## Files Created/Modified

### Created
1. **`backend/app.py`** - Added `/aqi/current` endpoint
2. **`indradhanu-frontend/src/components/AQIDisplay.jsx`** - New AQI component
3. **`test_aqi_endpoint.py`** - API test script
4. **`AQI_INTEGRATION.md`** - This documentation

### Modified
1. **`indradhanu-frontend/src/components/WeatherDashboard.jsx`** - Integrated AQI component

## Test Results

### ✅ Test Location: Mumbai, India
```
🌬️ Air Quality Index: 70
   Category: Moderate
   Color: #ffff00
   Dominant Pollutant: PM2.5

📊 Pollutant Breakdown:
   PM2.5: 70 μg/m³
   PM10: 27 μg/m³
   Ozone (O₃): 26.4 ppb
   Nitrogen Dioxide (NO₂): 24.7 ppb
   Sulfur Dioxide (SO₂): 4.1 ppb
   Carbon Monoxide (CO): 6.4 ppb

💡 Health Implications:
   Air quality is acceptable. However, there may be a risk 
   for some people, particularly those who are unusually 
   sensitive to air pollution.

⚠️ Cautionary Statement:
   Unusually sensitive people should consider limiting 
   prolonged outdoor exertion.
```

## How to Use

### 1. Navigate to Weather Page
```
http://localhost:3000/weather
```

### 2. Select a Location
- Search for a city
- Use current GPS location
- Click popular location chip
- Enter coordinates manually

### 3. Fetch Weather Data
Click "Fetch Data" or "Analyze" button

### 4. View AQI Information
The AQI card will appear automatically below the location info, showing:
- Current AQI value with color coding
- Health implications
- Cautionary statements
- Pollutant breakdown
- AQI scale reference

## API Usage & Limits

### Demo Token Limits
- **1000 requests/day** (shared across all users)
- Sufficient for development and testing
- Consider getting dedicated token for production

### Getting Your Own Token
1. Visit: https://aqicn.org/data-platform/token/
2. Register for free API token
3. Replace in `backend/app.py`:
   ```python
   waqi_token = "YOUR_TOKEN_HERE"
   ```

### Rate Limiting Recommendations
- Cache AQI data for 30-60 minutes
- Implement request throttling
- Monitor API usage
- Consider fallback data sources

## Health Implications by Category

### Good (0-50)
- ✅ Air quality is satisfactory
- ✅ No health concerns
- ✅ Safe for all outdoor activities

### Moderate (51-100)
- ⚠️ Acceptable for most people
- ⚠️ Unusually sensitive people should limit prolonged exertion
- ✅ Generally safe for outdoor activities

### Unhealthy for Sensitive Groups (101-150)
- ⚠️ Sensitive groups may experience health effects
- ⚠️ General public less likely to be affected
- 🚫 Sensitive groups should limit prolonged outdoor exertion

### Unhealthy (151-200)
- 🚫 Everyone may experience health effects
- 🚫 Sensitive groups may experience more serious effects
- 🚫 Everyone should limit prolonged outdoor exertion

### Very Unhealthy (201-300)
- 🚨 Health alert: Risk increased for everyone
- 🚨 Serious health effects for sensitive groups
- 🚫 Everyone should avoid prolonged outdoor exertion
- 🏠 Sensitive groups should remain indoors

### Hazardous (301+)
- 🚨 Emergency conditions
- 🚨 Everyone likely to be affected
- 🏠 Everyone should avoid all outdoor exertion
- 🚨 Stay indoors with air purification

## Troubleshooting

### Issue: "Failed to fetch AQI data"
**Solutions:**
- Check internet connection
- Verify coordinates are valid
- API token may have reached daily limit
- Try different location

### Issue: AQI component not showing
**Solutions:**
- Ensure weather data is fetched first
- Check browser console for errors
- Verify backend is running
- Check coordinates are valid

### Issue: Incorrect location name
**Solutions:**
- WAQI uses nearest monitoring station
- Station may be in different city/area
- This is normal and expected
- AQI value is still accurate for the region

## Benefits

### For Users
1. ✅ **Health Awareness** - Know when air quality is poor
2. ✅ **Activity Planning** - Plan outdoor activities safely
3. ✅ **Sensitive Groups** - Protect vulnerable populations
4. ✅ **Real-time Data** - Current air quality conditions
5. ✅ **Detailed Breakdown** - Understand specific pollutants

### For Platform
1. ✅ **Comprehensive Data** - Weather + Air Quality
2. ✅ **User Value** - Enhanced decision-making
3. ✅ **Health Focus** - Climate health impacts
4. ✅ **Professional** - Enterprise-grade features
5. ✅ **Global Coverage** - Works worldwide

## Status
✅ **FULLY INTEGRATED AND TESTED**

The AQI feature is now live on the Weather page with:
- Real-time air quality data
- Comprehensive health information
- Detailed pollutant breakdown
- Visual color-coded display
- Auto-refresh on location change

**Navigate to http://localhost:3000/weather to see it in action!** 🌬️
