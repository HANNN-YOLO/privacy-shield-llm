Today, I will be writing the code for the Address Detection feature.

The implementation runs entirely on the back-end because I am using Microsoft Presidio for analysis; this allows analysis results initially labeled as [LOC], [LOCATION], or [GPE] to be categorized as [ADDRESS]. This is made possible by the code examining the surrounding text—for instance, if words like "JL" or "Jakarta" are detected, the system captures the 40 characters preceding them and designates that segment as an [ADDRESS].
