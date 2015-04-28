# UQ Program Analysis
## Thomas Cranny

---

## What and Why?

--

### What?
Web-App (?) to analyse the programs UQ offers.

--

### Why?
- Doing a dual degree at UQ is confusing.
    - No course plan.
    - Two separate faculties to liaise with.

- Interesting and relevant data-set to me.

Note: Faculties seem happy to say "let the other faculty" handle it 

---

## Introduction to UQ

--

### UQ has six faculties:
1. **BEL**: Business, Economics and Law
2. **EAIT**: Engineering, Architecture, and IT
3. **HABS**: Health and Behavioural Sciences
4. **HASS**: Humanities and Social Sciences
5. **MBS**: Medicine and Biomedical Sciences
6. **Science**

--

### Faculties Offer Singular *Programs*:
*Degrees* or *Diplomas*

~100 single programs offered

--
### Programs Offer Majors
Specialisations on a topic

--

### Some programs can be done together
*Dual Degrees*, which are programs themselves.

--
### Dual Degrees
May have specific cross faculty Majors, or multiple from the constituent Programs.

~30 Dual Degree programs offered

---

# Analysis
## Faculties and Programs

--

![Programs offered by faculties](/static/presentation/images/faculty_degrees_trans.png)

---

## Where are the Dual Degrees being shared?

--

![Faculty relationships of degrees](/static/presentation/images/faculty_dual_degrees_trans.png)

Note: The HASS (Arts) band is brighter, showing it has many duals. As the previous graph showed, HABS does not share much.

---

## OP Scores

--

![Distribution of OP scores by faculty](/static/presentation/images/faculty_entry_ops_trans.png)

Note: HABS has the lowest cutoff, due to popularity?


---


## Program Fees

--

![Distribution of program fees by faculty](/static/presentation/images/faculty_fees_outliers_trans.png)

Note: 2 crazy outliers, EAIT one because of a glitch, but the valid price for international students doing a bachelor of
  Engineering (honours) **and** a Masters of Engineering.

--

![Distribution of program fees by faculty (with outliers removed)](/static/presentation/images/faculty_fees_no_outliers_trans.png)

Note:
- Science has a $5,000 higher median
- Law degrees in BEL pad out it's IQR however.
- Also seen is a cluster of outliers *under* the range for science degree prices; these are a small set of cheap, short diplomas.

---

## OP and Cost

--

![Distribution of program fees by faculty (with outliers removed)](/static/presentation/images/all_scatter_trans.png)

Note:
- Small amount of x-jitter to spread points.
- BEL: expensive and good OPs.
- HASS: not so much...
- Red strip for Expensive but easier to get into engineering degrees.