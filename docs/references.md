# References

Add each source when it is first used, and say what it's used for. Mark anything not yet checked.

## Used

- Bell, I. H., Wronski, J., Quoilin, S., Lemort, V. (2014). Pure and pseudo-pure fluid thermophysical property
  evaluation and the open-source thermophysical property library CoolProp. *Industrial & Engineering Chemistry
  Research*, 53(6), 2498–2508. Used for R-134a properties in `calcs/`.
- Esposito, A. *Fluid Power with Applications*. Pearson. Its vane pump displacement formula is compared in
  [functional-design.md](functional-design.md#displacement).
- Ansys Granta EduPack 2026 R1, Level 3 database. Materials screening and ranking in
  [materials.md](materials.md#selection-in-granta).
- Ansys Granta help, *Pass criteria for the stage (Pass when)*: "any part of record" vs "whole record" within
  selection, default "any part"
  (<https://ansyshelp.ansys.com/public/Views/Secured/Granta/v251/en/Selector/sel_edu/pass_criteria.html>), and
  *Default application settings*
  (<https://ansyshelp.ansys.com/public/Views/Secured/Granta/v261/en/Edu_Pack_Help/sel_edu/default_application_settings.html>).
  Used in [materials.md](materials.md#approach).
- Granta EduPack tutorial videos, YouTube playlist <https://www.youtube.com/playlist?list=PLtt6-ZgUFmMK4aApOU0A85CvaJ_udGDCe>.
  Suggested viewing order from the "Granta Video List" spreadsheet, with each video's number in the playlist:
  1. Basic Materials Selection (#10): <https://www.youtube.com/watch?v=ns1R5WSfz94>
  2. Main Toolbar (#5): <https://www.youtube.com/watch?v=SWF5wg3_wbw>
  3. Creating Charts (#1): <https://www.youtube.com/watch?v=oVH2r8tJrp8>
  4. Limit Stage (#3): <https://www.youtube.com/watch?v=PXNsSB4BHdI>
  5. Tree Stage (#4): <https://www.youtube.com/watch?v=AsZ7Px64s-o>
  6. Formatting Charts (#2): <https://www.youtube.com/watch?v=hNA5DBNwm1I>
  7. Advanced Charts (#6): <https://www.youtube.com/watch?v=RaFOvfQXLhM>
  8. Searching (#12): <https://www.youtube.com/watch?v=F7yDDxinbfQ>
  9. Browse Part 1: The Structure (#8): <https://www.youtube.com/watch?v=3CJ-cejsXFQ>
  10. Browse Part 2: The Data (#7): <https://www.youtube.com/watch?v=m5CJJh8LyYc>
  11. Browse Part 3: The Links (#9): <https://www.youtube.com/watch?v=mxsvdYGp4S0>
  12. Basic Eco Audit (#11): <https://www.youtube.com/watch?v=9qlw7JroxRY>
  13. Enhanced Eco Audit (#14): <https://www.youtube.com/watch?v=hGLL7waaiNg>
  14. Hybrid Material Synthesizer (#13): <https://www.youtube.com/watch?v=x7f2VxFrYxk>
  15. Part Cost Estimator (#15): <https://www.youtube.com/watch?v=-QOfJY89Rpw>
- Blackmer LGL3021 sliding-vane pump (LPG), materials table: ductile iron ASTM A536 casing, heads and rotor; cast
  iron ASTM A48 liner and discs; high-tensile steel shaft; Duravane vanes. Read through a search summary because the
  page blocked direct access (verify):
  <https://www.psgdover.com/blackmer/products/sliding-vane-pumps/lgl-series-sliding-vane-pumps/lgl3021-sliding-vane-pumps>.
  Used in [materials.md](materials.md#viable-material-families).
- Procon rotary vane pumps: carbon-graphite vanes, liners and bearings; brass or stainless housings; stainless rotor
  and shaft in some series. Procon catalog:
  <https://www.acomee.com.mx/catalogos/catalogosp/PROCON-PRODUCTS%20PUMPS%20CATALOG.pdf>; distributor listing:
  <https://www.raptorsupplies.com.au/p/procon/4-series-rotary-vane-pumps>.
- Rotary refrigerant compressor patents: high-speed tool steel vanes, nitrided or CrN/DLC coated, against gray or
  alloy cast iron; HFC refrigerants lubricate poorly. US 8,939,742 (steel and cast iron sliding materials),
  US 9,169,526, US 9,644,245; US 2013/0118651 (alloy cast iron vane).
- Liquid refrigerant pump literature (read through search summaries, verify against the documents): Buffalo Pumps
  refrigerant pumps, low-temperature ductile iron or cast steel casing with cast iron impeller, services include
  R-134a (<https://buffalopumps.com/index.php/download_file/view/1373/86>); Hansen HERMETIC CAM/CNF canned-motor pumps,
  ductile iron casing, rated −60 °F to 194 °F
  (<https://static1.squarespace.com/static/568fc9bac21b86decbc1965f/t/56eab26e07eaa03f5db7fed4/1458221680724/HermeticPump_bulletin.pdf>);
  Cornell CB refrigeration pumps, ductile iron with 304 stainless shaft
  (<https://www.keepsupply.com/2cb-4-2-3-1800-cornell-pump-2cb-close-coupled-pump-3hp-1800-rpm>). Used in
  [materials.md](materials.md#check-against-refrigerant-pumps).
- Rotary vane compressor patents: cast iron cylinder with steel or cast iron rotor and cast iron side plates (US
  4,526,524; US 5,356,277); aluminium body cast around a sintered iron liner (US 5,133,652); nodular iron vanes (US
  9,644,245).
- Course handout, *Final Report and Presentation* (headed ME500). Not kept in the repo; its content is recorded in
  [final deliverables](requirements.md#final-deliverables).

## To consult

- Ashby, M. F. *Materials Selection in Mechanical Design*. Butterworth-Heinemann. The selection method (translate,
  screen, rank, supporting information) and the performance indices in [materials.md](materials.md#selection-method).
- Budynas, R. G., Nisbett, J. K. *Shigley's Mechanical Engineering Design*. McGraw-Hill. Fatigue: endurance limit
  estimates, Marin correction factors, notch sensitivity. Needed for the infinite-life design in
  [functional-design.md](functional-design.md#fatigue).
- NSWC-11, *Handbook of Reliability Prediction Procedures for Mechanical Equipment*. Naval Surface Warfare Center.
  Component failure-rate models for the MTBF prediction ([D12](decisions.md)). Overview:
  <https://reliabilityeducation.com/intro-nswc.html>
- ISO 281, *Rolling bearings: Dynamic load ratings and rating life*. Defines L10.
- API Standard 610, *Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries*. Minimum bearing L10
  of 25,000 h at rated conditions and 16,000 h at maximum loads. Taken from secondary sources so far (e.g.
  <https://www.reliableplant.com/Articles/Print/22602>); check the standard text.
- Guiding values of basic bearing life: pumps in permanent operation 40,000–60,000 h
  (<https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-Help/files/GUID-D48016B4-90DC-42B2-8D0E-5DA01A36713A.htm>).
  Engineers Edge lists 50,000–60,000 h for machinery in continuous 24-hour service
  (<https://engineersedge.com/bearing/typical_bearing_life_14624.htm>). Bearing makers' catalogues are the primary
  source.
- ANSI/ASHRAE Standard 15 (Safety Standard for Refrigeration Systems) and Standard 34 (refrigerant designations and
  safety classification).
- UL 60335-2-34 (hermetic and semi-hermetic motor-compressors): check whether it applies to a semi-hermetic pump.
- Hydraulic Institute, Europump, US DOE. *Pump Life Cycle Costs: A Guide to LCC Analysis for Pumping Systems*.
  Framework for the repair-vs-swap decision in [serviceability.md](serviceability.md).
- US EPA, Clean Air Act Section 608: refrigerant recovery and the prohibition on venting.
- Eaton Vickers and Denison vane pump service literature: replacement cartridge kits as a model for the field repair
  kit.
- An elastomer compatibility chart (e.g. Parker O-Ring Handbook) for R-134a and POE oil.
- A hydraulics text giving the vane pump displacement form V = 2eL(πD − zt), to confirm the derivation.
- Manufacturer literature for canned-motor refrigerant pumps and for thin-fluid rotary vane pumps (analogs).
