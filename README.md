# q-importance
Python code to ranking daily reputation of public figure

## Usage
Run the below script and the result will be in output.csv
```
python OccurenceSeeker.py > result.csv
python csv_tranpose.py result.csv
```

## Public figures
Add public figures' name under any file in items_list, format is each name for one row. Please note that the name is treated as both public figure ID and seeker. Therefore, the current script is not able to distinguish two people with same name and also not able to map name alias.

## Import Your News
If you would like to run the program yourself, you should prepare a `tsv` with the format as below:
```
<Days_diff_from_2015/01/01>   <NEWS_TITLE>  <NEWS_CONTENT>
```
e.g., 
```
363	【李國章入主】李國章任校委會主席拆局　燙手山芋無人願接	港大校委會近期風波不絕，主席一職更是自梁智鴻卸任後，已懸空兩個月之久。特首梁振英最終⋯⋯
```

## Algorithm
The algorithm is going to illustrate the reputation based on the the following assumptions:
1. Reputation is decaying everyday if there is no update of the public figure ([forgetting curve](https://en.wikipedia.org/wiki/Forgetting_curve))
2. Public figure being reported recently is more reputable to others reported in the past
3. Public figure with more news results in higher reputation
4. Public figure with frequent news results in stabler reputation
5. Public figure being stated at the beginning in the article is more important to one being stated at the end
6. Public figure will remember others in the same article of itself

The algorithm is simply build a undirected graph that each vertex is representing a public figure and each edge is representing two public figures has appeared in the same news. The edge weight/distance is calculated according to the `forgetting curve` (details stated in reference). 

Based on the above graph, q-importance calculated the [closeness centrality](https://en.wikipedia.org/wiki/Closeness_centrality) for each vertex as a reputation value. User can rank the value to illustrate the relative repuation ranking between public figures.

## Reference 
Edge weight is calculated as: $$f\left(x\right)=500\left(1-1e^{-\frac{x}{S\cdot g^{0.25}}}\right)$$. Such that $$x$$ is the number day of the news reported and $$g$$ is as  $$\sum_{i=1}^n\sqrt{p_0p_1}$$ where $$p0$$ and $$p1$$ are the relative position of the two public figures in the article on that day. $$S$$ is the stable function aggregating all news before which is calculated by the function as $$S=20\cdot\left(2-e^{\left(-\frac{8k^s}{\left(x+1\right)}\right)}\right)$$ where $$k$$ is a similar function to $$g$$ in $$f(x)$$.
