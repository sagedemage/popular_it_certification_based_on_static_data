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

    column_names = ["Certification", "Average Number of Jobs", "Points"]

    in_popular_cert = {
        "RHCSA": False,
        "CCNA": False,
        "CompTIA Network+": False,
        "CompTIA Security+": False,
        "CompTIA Linux+": False,
    }

    popular_certs: List[List[str]] = []
    point = len(sorted_avgs)
    no_previous_value = True
    previous_point = 0
    previous_value = 0
    for i in range(len(sorted_avgs)):
        sort_avg = sorted_avgs[i]
        for key, val in means.items():
            if means[key] == sort_avg and in_popular_cert[key] == False:
                if no_previous_value == True:
                    row = [key, str(val), point-1*i]
                    popular_certs.append(row)
                    in_popular_cert[key] = True
                    previous_value = val
                    previous_point = point-1*i
                    no_previous_value = False
                    break
                if val < previous_value:
                    row = [key, str(val), previous_point-1]
                    popular_certs.append(row)
                    in_popular_cert[key] = True
                    previous_value = val
                    previous_point = previous_point-1
                    break
                if val == previous_value:
                    row = [key, str(val), previous_point]
                    popular_certs.append(row)
                    in_popular_cert[key] = True
                    previous_value = val
                    break

    save_data_to_csv_file(column_names, popular_certs, "gen_data/averages_of_it_certs.csv")
    
    popular_certs_table = Table(
        column_names=column_names,
        rows=popular_certs
    )
    return popular_certs_table


def get_it_certs_information() -> Table:
    """Implementation to get the IT certification information"""
    df = pd.read_csv("data/it_certs_info.csv")
    column_names = ["Certification", "Difficulty Level", "Exam Duration (min)", "Price", "Position", "Points"]
    cert = df["Certification"]
    diff_level = df["Difficulty Level"]
    exam_duration = df["Exam Duration (min)"]
    price = df["Price"]
    position = df["Position"]

    it_certs_info: List[List[str]] = []
    for i in range(len(cert)):
        point = None
        if diff_level[i] == "Beginner":
            point = 1
        elif diff_level[i] == "Intermediate":
            point = 2
        row = [cert[i], diff_level[i], exam_duration[i], price[i], position[i], point]
        it_certs_info.append(row)

    save_data_to_csv_file(column_names, it_certs_info, "gen_data/it_certs_info.csv")

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

    avg_of_it_certs = AvgITCerts(None, None, None)
    avg_of_it_certs.certs = avg_of_it_certs_df["Certification"]
    avg_of_it_certs.points = avg_of_it_certs_df["Points"]

    it_certs_info = ITCertsInfo(None, None, None)
    it_certs_info.certs = it_certs_info_df["Certification"]
    it_certs_info.points = it_certs_info_df["Points"]

    total_points_of_it_certs: List[List[str]] = []
    column_names = ["Certifications", "Total Points"]
    for i in range(len(avg_of_it_certs.certs)):
        avg_of_it_certs.cert = avg_of_it_certs.certs[i]
        for j in range(len(it_certs_info.certs)):
            it_certs_info.cert = it_certs_info.certs[j]
            if avg_of_it_certs.cert == it_certs_info.cert:
                sum = int(avg_of_it_certs.points[i]) + int(it_certs_info.points[j])
                total_points_of_it_certs.append([avg_of_it_certs.cert, sum])
                break

    save_data_to_csv_file(column_names, total_points_of_it_certs, "gen_data/total_points_of_it_certs.csv")

    total_points_of_it_certs_table = Table(
        column_names=column_names,
        rows=total_points_of_it_certs
    )
    return total_points_of_it_certs_table

def save_data_to_csv_file(column_names: List[str], data: List[List[str]], file_path: str):
    """Save the data containing the list of rows to a CSV file"""
    csv_data = {}
    for column in column_names:
        csv_data[column] = []

    for item in data:
        for i in range(len(column_names)):
            column = column_names[i]
            csv_data[column].append(item[i])

    df = pd.DataFrame.from_dict(csv_data)
    df.to_csv(file_path, index=False)

def main():
    print("\nIT Position Information:")
    df = pd.read_csv("data/it_position_info.csv")
    print(df.to_string(index=False))
    print("\nPosition Levels: Level 1 - Early Career, Level 2 - Mid Career, Level 3 - Late Career")
    
if __name__ == "__main__":
    main()