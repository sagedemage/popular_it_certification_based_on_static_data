# Main Flask Web Application
import pandas as pd
from flask import Flask, render_template
from typing import List
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class Table:
    column_names: List[str]
    rows: List[List[str]]

@app.route("/")
def home_page():
    popular_certs_table = get_averages_of_it_certs()
    it_certs_info_table = get_it_certs_information()
    it_position_info_table = get_it_position_information()

    template = render_template(
        'index.html', 
        popular_certs_table=popular_certs_table, 
        it_certs_info_table=it_certs_info_table,
        it_position_info_table=it_position_info_table,
        )
    return template

@app.route("/total-points-of-it-certs")
def total_points_of_it_certs():
    total_points_of_it_certs_table = get_total_points_of_it_certs()

    template = render_template(
        'total_points_of_it_certs.html', 
        total_points_of_it_certs_table=total_points_of_it_certs_table
        )
    return template

@app.route("/it-position-info")
def it_position_page():
    it_position_info_table = get_it_position_information()

    template = render_template(
        'it_position_info.html', 
        it_position_info_table=it_position_info_table
        )
    return template

def get_averages_of_it_certs() -> Table:
    """Implementation to get the popular IT certifications"""
    df = pd.read_csv("data/popular_it_certs_in_defense_companies.csv", index_col=False)

    average_of_it_certs_data = {
        "Certifications": [],
        "Average Number of Jobs": [],
    }

    certs = ["RHCSA", "CCNA", "CompTIA Network+", "CompTIA Security+", "CompTIA Linux+", "CompTIA A+"]

    means = {
        "RHCSA": int(df["RHCSA"].mean().__round__(-1)),
        "CCNA": int(df["CCNA"].mean().__round__(-1)),
        "CompTIA Network+": int(df["CompTIA Network+"].mean().__round__(-1)),
        "CompTIA Security+": int(df["CompTIA Security+"].mean().__round__(-1)),
        "CompTIA Linux+": int(df["CompTIA Linux+"].mean().__round__(-1)),
        "CompTIA A+": int(df["CompTIA A+"].mean().__round__(-1)),
    }

    for cert in certs:
        average_of_it_certs_data["Certifications"].append(cert)
        avg = means[cert]
        average_of_it_certs_data["Average Number of Jobs"].append(avg)

    column_names = ["Certifications", "Average Number of Jobs", "Points"]

    df_average_of_it_certs_data = pd.DataFrame(average_of_it_certs_data)
    df_average_of_it_certs_data = df_average_of_it_certs_data.sort_values(
        by=["Average Number of Jobs"],
        ascending=False
    )

    points = []
    i = len(df_average_of_it_certs_data["Certifications"])
    for _ in range(len(df_average_of_it_certs_data["Certifications"])):
        points.append(i)
        i = i - 1
    df_average_of_it_certs_data.insert(2, "Points", points)

    average_of_it_certs_data = df_average_of_it_certs_data.to_numpy()

    df_average_of_it_certs_data.to_csv("gen_data/averages_of_it_certs.csv", index=False)
    
    average_of_it_certs_data_table = Table(
        column_names=column_names,
        rows=average_of_it_certs_data
    )
    return average_of_it_certs_data_table


def get_it_certs_information() -> Table:
    """Implementation to get the IT certification information"""
    df_it_certs_info = pd.read_csv("data/it_certs_info.csv")
    column_names = ["Certifications", "Difficulty Level", "Exam Duration (min)", "Price", "Position", "Points"]
    diff_levels = df_it_certs_info["Difficulty Level"]

    points = []
    for diff_level in diff_levels:
        if diff_level == "Level 1 - Novice":
            point = -2
            points.append(point)
        elif diff_level == "Level 2 - Advanced Beginner":
            point = 2
            points.append(point)
        elif diff_level == "Level 3 - Intermediate":
            point = 4
            points.append(point)

    df_it_certs_info.insert(5, "Points", points)

    it_certs_info = df_it_certs_info.to_numpy()

    df_it_certs_info.to_csv("gen_data/it_certs_info.csv", index=False)

    it_certs_info_table = Table(
        column_names=column_names,
        rows=it_certs_info
    )

    return it_certs_info_table

def get_it_position_information() -> Table:
    """Implementation to get the IT certification information"""
    df = pd.read_csv("data/it_position_info.csv")
    column_names = ["Positions", "Position Level", "Average Annual Salary"]
    position = df["Positions"]
    position_level = df["Position Level"]
    avg_annual_salary = df["Average Annual Salary"]

    it_position_info: List[List[str]] = []
    for i in range(len(position)):
        row = [position[i], position_level[i], avg_annual_salary[i]]
        it_position_info.append(row)

    it_position_info_table = Table(
        column_names=column_names,
        rows=it_position_info
    )

    return it_position_info_table

@dataclass
class AvgITCerts:
    certs: List[str]
    points: List[str]
    cert: str

@dataclass 
class ITCertsInfo:
    certs: List[str]
    points: List[str]
    cert: str

def get_total_points_of_it_certs() -> Table:
    avg_of_it_certs_df = pd.read_csv("gen_data/averages_of_it_certs.csv")
    it_certs_info_df = pd.read_csv("gen_data/it_certs_info.csv")

    total_points_of_it_certs_data = {
        "Certifications": [],
        "Total Points": []
    }

    avg_of_it_certs = AvgITCerts(None, None, None)
    avg_of_it_certs.certs = avg_of_it_certs_df["Certifications"]
    avg_of_it_certs.points = avg_of_it_certs_df["Points"]

    it_certs_info = ITCertsInfo(None, None, None)
    it_certs_info.certs = it_certs_info_df["Certifications"]
    it_certs_info.points = it_certs_info_df["Points"]

    for i in range(len(avg_of_it_certs.certs)):
        avg_of_it_certs.cert = avg_of_it_certs.certs[i]
        for j in range(len(it_certs_info.certs)):
            it_certs_info.cert = it_certs_info.certs[j]
            if avg_of_it_certs.cert == it_certs_info.cert:
                sum = int(avg_of_it_certs.points[i]) + int(it_certs_info.points[j])
                total_points_of_it_certs_data["Certifications"].append(avg_of_it_certs.cert)
                total_points_of_it_certs_data["Total Points"].append(sum)
                break

    df_total_points_of_it_certs_data = pd.DataFrame(total_points_of_it_certs_data)
    df_total_points_of_it_certs_data = df_total_points_of_it_certs_data.sort_values(
        by=["Total Points"],
        ascending=False
    )

    column_names = ["Certifications", "Total Points"]
    total_points_of_it_certs = df_total_points_of_it_certs_data.to_numpy()

    df_total_points_of_it_certs_data.to_csv("gen_data/total_points_of_it_certs.csv", index=False)

    total_points_of_it_certs_table = Table(
        column_names=column_names,
        rows=total_points_of_it_certs
    )
    return total_points_of_it_certs_table

def main():
    print("\nIT Position Information:")
    df = pd.read_csv("data/it_position_info.csv")
    print(df.to_string(index=False))
    print("\nPosition Levels: Level 1 - Early Career, Level 2 - Mid Career, Level 3 - Late Career")
    
if __name__ == "__main__":
    main()