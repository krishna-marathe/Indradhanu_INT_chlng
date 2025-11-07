# 🔑 Getting a WAQI API Token for Accurate AQI Data

## Current Limitation

The system currently uses the **demo token** from WAQI (World Air Quality Index) API, which has limitations:
- ⚠️ Returns data from distant monitoring stations
- ⚠️ May show Shanghai station for all locations
- ⚠️ Limited to 1000 requests/day (shared globally)
- ⚠️ Not suitable for production use

## Solution: Get Your Own API Token

### Step 1: Register for Free Token

1. **Visit**: https://aqicn.org/data-platform/token/
2. **Fill out the form**:
   - Name
   - Email address
   - Organization (optional)
   - Purpose: "Climate analytics platform"
3. **Submit** and check your email
4. **Receive your token** (usually instant)

### Step 2: Add Token to Backend

#### Option A: Environment Variable (Recommended)

1. Open `backend/.env` file
2. Add your token:
   ```env
   WAQI_API_TOKEN=your_actual_token_here
   ```

#### Option B: Direct in Code

1. Open `backend/app.py`
2. Find this line:
   ```python
   waqi_token = os.getenv('WAQI_API_TOKEN', 'demo')
   ```
3. Replace with:
   ```python
   waqi_token = "your_actual_token_here"
   ```

### Step 3: Restart Backend

```bash
# Stop the current backend
# Then restart
python backend/app.py
```

### Step 4: Test

```bash
python test_aqi_endpoint.py
```

You should now see:
- ✅ Correct local monitoring stations
- ✅ Accurate distances (< 50 km typically)
- ✅ More reliable AQI data
- ✅ Higher request limits

## Benefits of Your Own Token

| Feature | Demo Token | Your Token |
|---------|-----------|------------|
| **Monitoring Stations** | Distant (1000s of km) | Local (< 50 km) |
| **Accuracy** | Low | High |
| **Request Limit** | 1000/day (shared) | 1000/day (dedicated) |
| **Reliability** | Low | High |
| **Production Ready** | ❌ No | ✅ Yes |

## Free Tier Limits

- **1000 requests per day**
- **Sufficient for**:
  - Small to medium applications
  - Development and testing
  - Personal projects
  - Educational use

## Paid Plans (Optional)

For higher limits, visit: https://aqicn.org/data-platform/pricing/

- **Basic**: 10,000 requests/day
- **Pro**: 100,000 requests/day
- **Enterprise**: Custom limits

## Current Workaround

Until you get your own token, the system:
1. ✅ Shows the **correct location name** (Mumbai, Delhi, etc.)
2. ✅ Displays the **monitoring station name** (e.g., Shanghai)
3. ✅ Shows the **distance** to the monitoring station
4. ⚠️ Displays a **warning** when station is > 100 km away
5. ✅ Still provides **useful AQI estimates**

## Alternative AQI APIs

If WAQI doesn't work for your region, consider:

### 1. OpenWeatherMap Air Pollution API
- **Website**: https://openweathermap.org/api/air-pollution
- **Free Tier**: 1000 calls/day
- **Coverage**: Global
- **Data**: PM2.5, PM10, O₃, NO₂, SO₂, CO

### 2. IQAir API
- **Website**: https://www.iqair.com/air-pollution-data-api
- **Free Tier**: Limited
- **Coverage**: Global
- **Data**: Comprehensive AQI

### 3. AirNow API (USA Only)
- **Website**: https://docs.airnowapi.org/
- **Free**: Yes
- **Coverage**: USA only
- **Data**: Official EPA data

## Implementation Status

✅ **Current**: Demo token with distance warnings
🔄 **Recommended**: Get your own WAQI token
🚀 **Production**: Use dedicated token or paid plan

## Questions?

- **WAQI Documentation**: https://aqicn.org/json-api/doc/
- **Support**: https://aqicn.org/contact/
- **Status**: https://aqicn.org/status/

---

**Note**: The current implementation works but shows distant monitoring stations. Getting your own token takes 2 minutes and provides much better data!
