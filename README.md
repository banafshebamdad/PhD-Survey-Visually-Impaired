# Navigating Independence: A Survey of Visually Impaired People’s Experiences and Needs

This repository accompanies the research paper: Navigating Independence: A Survey of Visually Impaired People’s Experiences and Needs

The paper reports the results of a fully accessible, globally distributed online
survey investigating navigation experiences, challenges, and assistive
technology preferences of blind and visually impaired (BVI) individuals.

This repository provides public access to the survey questionnaire and
supporting documentation referenced in the paper.

---

## Overview of the Study

Independent navigation in unfamiliar environments remains a major challenge for
blind and visually impaired individuals. While a wide range of assistive
navigation technologies exists, their adoption and effectiveness in everyday
settings vary significantly.

The study presented in the accompanying paper is based on:
- A fully accessible online questionnaire
- 17 closed-ended and 2 open-ended questions
- Global dissemination through organizations and individual contacts supporting
  visually impaired communities
- 42 completed responses from participants with varying degrees of visual
  impairment

The survey captures:
- Navigation experiences in unfamiliar environments
- Use and non-use of assistive navigation technologies
- Reported challenges such as obstacle detection and wayfinding
- Preferences regarding device form factors and feedback modalities
- User expectations and design considerations expressed in open-ended responses

The analysis combines descriptive quantitative statistics with qualitative
inductive thematic analysis of open-ended responses.

---

## Repository Contents

### Paper
- [Preprint version of the survey paper](Navigating_Independence__A_Survey_of_Visually_Impaired_People_s_Experiences_and_Needs-2.pdf) 

### Questionnaire
- [`questionnaire`](questionnaire/): Accessible HTML version of the survey questionnaire (screen-reader compatible).
- [`questionnaire.md`](https://github.com/banafshebamdad/PhD-Survey-Visually-Impaired/wiki/questionnaire): Markdown version of the questionnaire for direct inspection on GitHub.
- `questionnaire/questionnaire.pdf`: Reference PDF version of the questionnaire.

### Data
- `data/raw/responses_anonymized.csv`: Anonymized survey responses.
- `data/processed/summary_statistics.csv`: Aggregated counts, percentages, and derived statistics reported in the paper.
- `data/README.md`: Description of data fields, preprocessing, and anonymization steps.

### Analysis
- `analysis/analysis_description.md`: Description of quantitative and qualitative analysis procedures, including:
  - Percentage and count reporting
  - Use of Wilson score intervals for 95% confidence intervals
  - Inductive thematic analysis of open-ended responses
- `analysis/confidence_intervals.md`: Explanation of the Wilson 95% confidence interval method used for key
  proportions.

### Recruitment
- `recruitment/organizations_list.md`: High-level description of recruitment channels and organization types involved
  in survey dissemination. Individual names are intentionally omitted to protect
  privacy.

### Ethics
- `ethics/ethics_statement.md`: Statement outlining informed consent, anonymity, and ethical handling of
  participant data.

---

## Accessibility

Accessibility was a central design requirement of the study.  
The questionnaire was designed to be fully accessible and was:
- Tested with screen readers
- Reviewed by a blind individual for usability and accessibility
- Evaluated using accessibility tools (WAVE)

---

## Data Privacy and Ethics

- Participation was voluntary.
- Eligibility was based on self-identification as blind or visually impaired.
- No personally identifiable information was collected or retained.
- Duplicate, test, and incomplete responses were removed prior to analysis.
- Only anonymized and aggregated data are included in this repository.

This repository does not contain raw identifiable data, contact information, or
private communications.

---

## Citation

If you use any material from this repository, please cite the associated paper:

> Bamdad, M. (2026). *Navigating Independence: A Survey of Visually Impaired
> People’s Experiences and Needs.*

(Full bibliographic details will be updated upon publication.)

---

## License

This repository is intended for academic and research use.
