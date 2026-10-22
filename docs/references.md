# References

Add each source when it is first used, and say what it's used for. Mark anything not yet checked.

## Used

- Bell, I. H., Wronski, J., Quoilin, S., Lemort, V. (2014). Pure and pseudo-pure fluid thermophysical property
  evaluation and the open-source thermophysical property library CoolProp. *Industrial & Engineering Chemistry
  Research*, 53(6), 2498–2508. Used for R-134a properties in `calcs/`.
- Esposito, A. *Fluid Power with Applications*. Pearson. Its vane pump displacement formula is compared in
  [functional-design.md](functional-design.md#displacement).

## To consult

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
