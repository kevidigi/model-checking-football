# Model Checking for Strategy Generation in Football

Senior Honours Dissertation Project | BSc (Hons) Software Engineering | University of Glasgow

## Abstract


In his 2008 retrospective of the sport, Inverting the Pyramid, Jonathan Wilson observed that football practitioners, particularly in the UK, have traditionally been "unwilling to grapple with the abstract." In the past decade, however, abstractions of football have become invaluable. Teams increasingly rely on computer-aided analysis of match data to inform decisions, both on and off the pitch. This project investigates the feasibility of using model checking as a technique to gain insights from football data and identify potential strategies.
We show that event-level match data can be used in conjunction with modelling techniques and the PRISM probabilistic model checker to synthesise plausible football strategies, and attempt to lay a foundation for potential future work on this topic.

---

Datasets available from: https://figshare.com/collections/Soccer_match_event_dataset/4415000/2

(Pappalardo, L., Cintia, P., Rossi, A. et al.; A public data set of spatio-temporal match events in soccer competitions; Sci Data 6, 236 (2019). https://doi.org/10.1038/s41597-019-0247-7)

To generate models:
* Clone the repository
* Download "events_Italy.json", "events_France.json", "events_Spain.json", "events_Germany.json" and "events_England.json" from the datasets above
* Create a directory in the project root called "data" and place the .json files inside it
* Run "code/python/extract_wyscout_data.py" to generate PRISM files in "code/prism/"

---

## Conclusions

Probabilistic model checking has been shown to be a powerful tool for the simulation of very complex systems and the synthesis of strategies for the agents that control them. In this study we have made inroads to its application for the analysis of football, and potentially other similar team sports. We have demonstrated that even with a rudimentary model of possession in football, PRISM is capable of generating recognisable, viable strategies for maximum scoring potential, and identified areas where our work can be improved.

Future work that could build immediately upon the work herein could include: refinement of our model building process and the models themselves; extending the models to make use of PRISM’s reward structures; verifying the models with more complex properties and queries. We also suggest that data on team formations could drastically increase the value of the insights provided by our methods.
