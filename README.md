# pyFastAPI_PIP

A Tutorial to show how to build simple **Point-In-Polygon(PIP)** Web API using FastAPI and other python packages.

## Background

On year ago, I built an early warning service where the core algorithm is to use point data to find the area it belongs to.  It is a typical application of **point in polygon(PIP)**. In essence, it is also a reverse geocoding process, which converts the latitude and longitude coordinates to a readable address. In our service, we only care about national and provincial administrative boundaries. It is a simplified reverse geocoding process. 

## FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. The speed of the framework is compared with other competitors like NodeJS or Go. Also is fast to code (you’ll see this in a moment), easy to understand, intuitive and robust.

## Aim

In this tutorial, let's build a simple PIP web API using FastAPI and other python packages. 

Our APIs only focus on two Reverse Geocoding functions:
- pip

Single point query. This API returns the State and Country where the point is inside.

- pips

Multi-point query. This API only return the States and Countries where the points are inside without the points over ocean.

I put a detailed description in a PDF file or refer to 
https://www.linkedin.com/pulse/build-simple-reverse-geocoding-api-using-fastapi-chonghua-yin/?trackingId=weSAcTmflBWcZX%2BixZFmcg%3D%3D

The service could be started as

> python main.py

## Note
The test is too big to upload. You can download it and preprocess following the steps in the PDF file.

