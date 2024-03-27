# Monitoring Setup with Grafana, Prometheus, and k6

## Description

This project sets up a monitoring environment using Grafana for visualization, Prometheus for data collection, and k6 for load testing.

## Prerequisites

Before you begin, make sure you have Docker installed on your machine.

## Usage

1. Clone the repository to your local machine
2. Edit the load test in the `test.js` file in the `test` folder
3. Run Docker Compose to start the services
4. To visualize the test after it has finished running, creat a Grafana dashboard. An already created dashboard is present in the `grafana-dashboard.json` file. Copy the json content and paste in the space provided by Grafana.
