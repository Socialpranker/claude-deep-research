# Climate & environment

Climate, emissions, environmental data. ESG sustainability — см. `industries/esg_sustainability.md`.

## Emissions / Climate

### Our World in Data — CO2 and Greenhouse Gas Emissions
**URL:** ourworldindata.org/co2-emissions
**Access:** OPEN
**What:** Curated CO2/GHG emissions by country, sector, time series. Per capita, cumulative
**When:** emission claims, country comparison
**Quality:** A (gateway к primary sources, e.g., Global Carbon Project)
**Combine with:** Climate TRACE для independent verification

### Climate TRACE
**URL:** climatetrace.org
**Access:** OPEN
**What:** Independent emissions tracking via satellite — facility-level
**When:** validation of self-reported emissions, granular data
**Quality:** A (independent methodology)
**Unique:** не зависит от country self-reports

### Global Carbon Project
**URL:** globalcarbonproject.org
**Access:** OPEN
**What:** Annual global carbon budget — emissions, sinks, fluxes
**When:** macro climate analysis
**Quality:** A — научный consortium

### EDGAR (Emissions Database for Global Atmospheric Research)
**URL:** edgar.jrc.ec.europa.eu
**Access:** OPEN
**What:** EU JRC emissions database — historical, per country, per sector
**When:** detailed emission analysis EU + global

## Temperature / Weather

### NOAA
**URL:** ncei.noaa.gov
**Access:** OPEN
**What:** Climate data, temperature records, weather extremes (US + global)
**When:** climate change claims, temperature trends
**Quality:** A

### Berkeley Earth
**URL:** berkeleyearth.org/data
**Access:** OPEN
**What:** Independent temperature records, methodology transparent
**When:** alternative to NOAA/NASA для cross-validation

### NASA GISS
**URL:** data.giss.nasa.gov/gistemp
**Access:** OPEN
**What:** Global surface temperature analysis
**When:** climate change validation

### Copernicus Climate Change Service
**URL:** climate.copernicus.eu/climate-data
**Access:** OPEN
**What:** EU climate service — comprehensive climate data including reanalysis
**When:** detailed climate research, projection scenarios

### IPCC Reports
**URL:** ipcc.ch
**Access:** OPEN
**What:** IPCC assessment reports — comprehensive climate science synthesis
**When:** authoritative climate science statements
**Quality:** A — peer-reviewed consensus

## Air quality

### EPA Air Quality
**URL:** epa.gov/air-quality-management/air-quality-monitoring-data
**Access:** OPEN
**What:** US air quality monitoring data
**When:** US air pollution research

### IQAir / WHO Air Quality
**URL:** iqair.com, who.int/data/gho/data/themes/air-pollution
**Access:** OPEN
**What:** Global air quality including PM2.5
**When:** global air pollution comparison

### European Environment Agency
**URL:** eea.europa.eu/data-and-maps
**Access:** OPEN
**What:** EU environmental data
**When:** EU environmental research

## Biodiversity / Ecosystems

### IUCN Red List
**URL:** iucnredlist.org
**Access:** OPEN
**What:** Species conservation status
**When:** biodiversity, endangered species claims

### GBIF (Global Biodiversity Information Facility)
**URL:** gbif.org
**Access:** OPEN
**What:** Species occurrence data globally
**When:** species range, biogeography

### Living Planet Index (WWF)
**URL:** livingplanetindex.org
**Access:** OPEN
**What:** Wildlife populations indicator
**When:** biodiversity trend research

## Energy data (climate-relevant)

### IEA
**URL:** iea.org/data-and-statistics
**Access:** PARTIAL OPEN (many free reports)
**What:** Global energy data — supply, demand, prices, carbon intensity
**When:** energy transition research

### BP Statistical Review (now Energy Institute)
**URL:** energyinstitute.org/statistical-review
**Access:** OPEN
**What:** Annual statistical review of world energy
**When:** historical energy data, fuel mix by country

### EIA (US Energy Information Admin)
**URL:** eia.gov
**Access:** OPEN
**What:** US energy detailed
**When:** US energy research
**См. также:** industries/energy.md

## Water

### AQUASTAT (FAO Water)
**URL:** fao.org/aquastat
**Access:** OPEN
**What:** Global water resources data
**When:** water resource analysis

### World Resources Institute
**URL:** wri.org/data
**Access:** OPEN
**What:** Environmental data tools (Aqueduct for water risk, Global Forest Watch)
**When:** water risk, deforestation, biodiversity

## Forests / Land use

### Global Forest Watch
**URL:** globalforestwatch.org
**Access:** OPEN
**What:** Forest cover change satellite data
**When:** deforestation claims, forest health

### MapBiomas
**URL:** mapbiomas.org
**Access:** OPEN
**What:** Land use / land cover change (Brazil, expanding global)
**When:** land use change analysis

## Climate commitments tracker

### Climate Action Tracker
**URL:** climateactiontracker.org
**Access:** OPEN
**What:** Country climate commitments evaluation
**When:** policy compliance analysis

### NDC Tracker
**URL:** climatewatchdata.org
**Access:** OPEN
**What:** Nationally Determined Contributions data
**When:** Paris Agreement compliance research

### SBTi (Science Based Targets)
**URL:** sciencebasedtargets.org/companies-taking-action
**Access:** OPEN
**What:** Companies with science-based climate targets
**When:** corporate climate commitments validation

## Quick reference

| Что ищем | Источник |
|---|---|
| CO2 emissions by country | OWID + Global Carbon Project |
| Independent emission verification | Climate TRACE (satellite) |
| Temperature record | NOAA + Berkeley Earth + NASA GISS (triangulate) |
| Climate science consensus | IPCC reports |
| Air quality | IQAir + WHO + EPA (US) + EEA (EU) |
| Endangered species | IUCN Red List |
| Global energy mix | IEA + BP/Energy Institute Statistical Review |
| Deforestation | Global Forest Watch |
| Country climate commitments | Climate Action Tracker |
| Corporate climate targets | SBTi |

## Critical reminders

- **Methodology matters.** Climate data — different agencies use different methodologies, may differ by ±0.1°C / 5% emissions. Cite multiple.
- **Self-reported emissions** unreliable. Climate TRACE satellite > national inventory для verification.
- **Climate skeptics' arguments** — большинство debunked. Strong consensus + lots of evidence. Apply standard validation (см. validate.md blocks).

## Combining patterns

**Country emissions claim:**
OWID (gateway) + Global Carbon Project (raw) + Climate TRACE (satellite verification) + national inventory (official self-report) — triangulate

**Climate change validation:**
IPCC reports (consensus) + NOAA + Berkeley Earth + NASA GISS (multiple temperature records) + Copernicus (reanalysis)

**Corporate climate claims:**
SBTi (validated targets) + CDP (disclosure) + company sustainability report + independent ratings (Sustainalytics — partial) + Climate TRACE (facility emissions если applicable)
