# Web Scrapper using Selenium
import pandas as pd
from flask import Flask, render_template
from typing import List, Dict, Tuple
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class Table:
    column_names: List[str]
    rows: List[List[str]]

@app.route("/")
def home_page():
    popular_certs_table = get_sorted_averages_of_popular_it_certs()
    it_certs_info_table = get_it_certs_information()
    it_position_info_table = get_it_position_information()

    template = render_template(
        'index.html', 
        popular_certs_table=popular_certs_table, 
        it_certs_info_table=it_certs_info_table,
        it_position_info_table=it_position_info_table
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

def get_sorted_averages_of_popular_it_certs() -> Table:
    """Implementation to get the popular IT certifications"""
    # This implementation sorts the mean of the number of jobs 
    # of the IT certifications from greatest to least
    df = pd.read_csv("data/popular_it_certs_in_defense_companies.csv", index_col=False)

    sorted_avgs = []

    means = {
        "RHCSA": int(df["RHCSA"].mean().__round__(-1)),
        "CCNA": int(df["CCNA"].mean().__round__(-1)),
        "CompTIA Network+": int(df["CompTIA Network+"].mean().__round__(-1)),
        "CompTIA Security+": int(df["CompTIA Security+"].mean().__round__(-1)),
        "CompTIA Linux+": int(df["CompTIA Linux+"].mean().__round__(-1)),
    }

    sorted_avgs.append(means["RHCSA"])
    sorted_avgs.append(means["CCNA"])
    sorted_avgs.append(means["CompTIA Network+"])
    sorted_avgs.append(means["CompTIA Security+"])
    sorted_avgs.append(means["CompTIA Linux+"])

    sorted_avgs.sort()
    sorted_avgs.reverse()

    column_names = ["Certification", "Average Number of Jobs"]

    in_popular_cert = {
        "RHCSA": False,
        "CCNA": False,
        "CompTIA Network+": False,
        "CompTIA Security+": False,
        "CompTIA Linux+": False,
    }

    popular_certs: List[List[str]] = []
    for sort_avg in sorted_avgs:
        for key, val in means.items():
            if means[key] == sort_avg and in_popular_cert[key] == False:
                row = [key, str(val)]
                popular_certs.append(row)
                in_popular_cert[key] = True
                break

    popular_certs_table = Table(
        column_names=column_names,
        rows=popular_certs
    )
    return popular_certs_table


def get_it_certs_information() -> Table:
    """Implementation to get the IT certification information"""
    df = pd.read_csv("data/it_certs_info.csv")
    column_names = ["Certification", "Difficulty Level", "Exam Duration (min)", "Price", "Position"]
    cert = df["Certification"]
    diff_level = df["Difficulty Level"]
    exam_duration = df["Exam Duration (min)"]
    price = df["Price"]
    position = df["Position"]

    it_certs_info: List[List[str]] = []
    for i in range(len(cert)):
        row = [cert[i], diff_level[i], exam_duration[i], price[i], position[i]]
        it_certs_info.append(row)

    it_certs_info_table = Table(
        column_names=column_names,
        rows=it_certs_info
    )

    return it_certs_info_table

def get_it_position_information() -> Table:
    """Implementation to get the IT certification information"""
    df = pd.read_csv("data/it_position_info.csv")
    column_names = ["Position", "Position Level", "Average Annual Salary"]
    position = df["Position"]
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

def main():
    print("\nIT Position Information:")
    df = pd.read_csv("data/it_position_info.csv")
    print(df.to_string(index=False))
    print("\nPosition Levels: Level 1 - Early Career, Level 2 - Mid Career, Level 3 - Late Career")
    
if __name__ == "__main__":
    main()