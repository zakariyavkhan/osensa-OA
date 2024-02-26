import argparse, requests, time


def sample_aqi(url, sample_period, sample_rate):
    aqi_vals = num_results = 0
    num_samples = sample_period * sample_rate

    # sampling loop
    for _ in range(num_samples):
        response = requests.get(url)

        if response.status_code != 200:
            print("Error with API request: ", response.status_code)
            return

        else:
            results = response.json()

            # this accounts for the case where different # of stations report at different sample points
            num_results += len(results["data"])

            for result in results["data"]:
                aqi_vals += int(result["aqi"])

                # at each sample point, print the station name and the aqi value
                print(f"{result['station']['name']}: {result['aqi']}")

            time.sleep(60 / sample_rate)

    return aqi_vals / num_results


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Sample AQI data")
    parser.add_argument(
        "--lat1",
        type=float,
        required=True,
        help="Latitude of the first point",
    )
    parser.add_argument(
        "--lng1",
        type=float,
        required=True,
        help="Longitude of the first point",
    )
    parser.add_argument(
        "--lat2",
        type=float,
        required=True,
        help="Latitude of the second point",
    )
    parser.add_argument(
        "--lng2",
        type=float,
        required=True,
        help="Longitude of the second point",
    )
    parser.add_argument(
        "--period", 
        type=int, 
        default=5, 
        help="Sample period in minutes"
    )
    parser.add_argument(
        "--rate", 
        type=int, 
        default=1, 
        help="Sample rate in samples per minute"
    )
    args = parser.parse_args()

    # Some error checking
    if args.period <= 0 or args.rate <= 0:
        print("Invalid period or rate")
        return

    url = f"https://api.waqi.info/v2/map/bounds?token={API_TOKEN}&latlng={args.lat1},{args.lng1},{args.lat2},{args.lng2}"

    # Sample AQI data
    print(f"\nAverage over all stations: {sample_aqi(url, args.period, args.rate)}")


if __name__ == "__main__":
    main()
