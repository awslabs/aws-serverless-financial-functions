## AWS Serverless Financial Functions

This is a collection of serverless apps that wrap common financial functions in AWS Lambda functions. The financial functions' names and interfaces are identical to the corresponding functions in Microsoft Excel for convenience.

In addition to the individual function apps, an API app is included, which stands up an Amazon API Gateway REST endpoint surfacing all of the functions.

### Financial Functions

1. FV - Returns the future value of an investment based on periodic, constant payments and a constant interest rate.
1. FVSCHEDULE - Returns the future value of an initial principal after applying a series of compound interest rates.
1. PV - Returns the present value of an investment: the total amount that a series of future payments is worth now.
1. NPV - Returns the net present value of an investment based on a discount rate and a series of future payments (negative values) and income (positive values).
1. XNPV - Returns the net present value for a schedule of cash flows.
1. PMT - Calculates the payment for a loan based on constant payments and a constant interest rate.
1. PPMT - Returns the payment on the principal for a given investment based on periodic, constant payments and a constant interest rate.
1. IRR - Returns the internal rate of return for a series of cash flows.
1. MIRR - Returns the internal rate of return for a series of periodic cash flows, considering both cost of investment and interest on reinvestment of cash.
1. XIRR - Returns the internal rate of return for a schedule of cash flows.
1. NPER - Returns the number of periods for an investment based on periodic, constant payments and a constant interest rate.
1. RATE - Returns the interest rate per period of a loan or an investment. For example, use 6%/4 for quarterly payments at 6% APR.
1. EFFECT - Returns the effective annual interest rate.
1. NOMINAL - Returns the annual nominal interest rate.
1. SLN - Returns the straight-line depreciation of an asset for one period.

## Installation Steps

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Search for the desired financial function application in [the AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications?query=aws-serverless-financial-functions)
1. Click on the desired financial function application and click "Deploy"

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
