import graphviz
import csv
import sys
from datetime import datetime

currentYear = datetime.now().year

father_mother_points = set()
direct_family = {}

dot = graphviz.Graph()

dot.attr(
    fontname="Helvetica,Arial,sans-serif",
    splines="polyline",
    nodesep="0.3",
    ranksep="1.85 equally", #equally
)

with open("SeaWorldOrcas.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)

    sorted_list = sorted(reader, key=lambda row: (row[-1], row[1]), reverse=False)

    for row in sorted_list:

        row = [r.replace(" ", "") for r in row]

        name, sex, father, mother, capture, dead = row[0], row[1], row[2], row[3], row[4], row[5] == "y"

        dob_capture = row[-1]

        if "-" in name:
            name = name.split("-")[-1]
            # continue

        if sex == "f":
            color, fillcolor = "red", "pink"
        elif sex == "m":
            color, fillcolor = "blue", "lightblue"
        else:
            color, fillcolor = "black", "white"

        if dead:
            fillcolor = "Gainsboro"

        father_mother_point = mother + father

        if father_mother_point != "":
        #if whale_name in father_mother_point:
            if not father_mother_point in father_mother_points:
                father_mother_points.add(father_mother_point)
                dot.node(father_mother_point, shape="point", penwidth="6")
                dot.edge(father, father_mother_point)
                dot.edge(mother, father_mother_point)
            dot.edge(father_mother_point, name)


        age = currentYear-int(dob_capture)

        #if name == whale_name or whale_name in father_mother_point:
        if True:
            dot.node(
                name,
                fixedsize="true",
                width="1.3",
                # label=f"{name}\n{age}",
                shape="box",
                color=color,
                fillcolor=fillcolor,
                style="filled, rounded",
                penwidth="2",
            )


# print(dot)
f = open("graph.dot", "w")
f.write(str(dot))
f.close()
dot.render("graph", view=True)
