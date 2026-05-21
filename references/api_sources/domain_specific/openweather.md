# OpenWeather API

## Overview

- **Endpoint base:** `https://api.openweathermap.org/data/`
- **Auth:** API key
- **Free tier:** 60 req/min, 1M calls/month
- **Docs:** https://openweathermap.org/api
- **Coverage:** Global weather + historical

## Auth setup

1. https://openweathermap.org/api → register
2. `export OPENWEATHER_KEY="..."`

## Query patterns

### Current weather

```
GET /2.5/weather?q={city}&appid={key}&units=metric
```

### Forecast 5-day

```
GET /2.5/forecast?q={city}&appid={key}&units=metric
```

### Historical (paid tier)

```
GET /3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={key}
```

## Use cases

- Climate research (current conditions)
- Logistics planning (weather affecting operations)
- Historical correlation analysis

## Combine with

- **NOAA** — для US historical detailed
- **Copernicus Climate** — для EU reanalysis
- **Berkeley Earth** — для long-term temperature records

## Notes

- OpenWeather — convenient но fairly basic
- Для serious climate research use NOAA/Berkeley/Copernicus
