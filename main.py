# Web Scrapper using Selenium
import pandas as pd

def main():
    # CompTIA A+,CompTIA Network+,RHCSA,CCNA,CCNP,CompTIA Security+,CompTIA CySA+,CISSP
    df = pd.read_csv("data/popular_it_certs_in_defense_companies.csv", index_col=False)

    sorted_avgs = []

    means = {
        "CompTIA Network+": int(df["CompTIA Network+"].mean()),
        "RHCSA": int(df["RHCSA"].mean()),
        "CCNA": int(df["CCNA"].mean()),
        "CompTIA Security+": int(df["CompTIA Security+"].mean()),
        "CompTIA Linux+": int(df["CompTIA Linux+"].mean()),
    }

    sorted_avgs.append(means["CompTIA Network+"])
    sorted_avgs.append(means["RHCSA"])
    sorted_avgs.append(means["CCNA"])
    sorted_avgs.append(means["CompTIA Security+"])
    sorted_avgs.append(means["CompTIA Linux+"])

    sorted_avgs.sort()
    sorted_avgs.reverse()

    sorted_certs = {"Cert": [], "Average Number of Jobs": []}
    for sort_avg in sorted_avgs:
        for key, val in means.items():
            if means[key] == sort_avg:
                sorted_certs["Cert"].append(key)
                sorted_certs["Average Number of Jobs"].append(val)
                break

    print("Popular IT Certifications in the Defense Industry:")
    sorted_certs_df = pd.DataFrame.from_dict(sorted_certs)
    print(sorted_certs_df.to_string(index=False))

    print("\nIT Certification Information:")
    df = pd.read_csv("data/it_certs_info.csv")
    print(df.to_string(index=False))
    print("\nNote: The CompTIA Security+ is a great certification for any position in the Defense industry.")
    
if __name__ == "__main__":
    main()