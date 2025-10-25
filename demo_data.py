"""
Demo data for testing the IP Valuation app without API credits
"""

DEMO_COMPANIES = {
    'AAPL': {
        'name': 'Apple Inc.',
        'segmented_revenues': [
            {
                'ticker': 'AAPL',
                'period': 'annual',
                'report_period': '2024-09-28',
                'items': [
                    {
                        'name': 'Revenue',
                        'amount': 201183000000.0,
                        'segments': [{'key': 'aapl:IPhoneMember', 'label': 'IPhone', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 29984000000.0,
                        'segments': [{'key': 'aapl:MacMember', 'label': 'Mac', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 26694000000.0,
                        'segments': [{'key': 'aapl:IPadMember', 'label': 'IPad', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 96169000000.0,
                        'segments': [{'key': 'us-gaap:ServiceMember', 'label': 'Services', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 37005000000.0,
                        'segments': [{'key': 'aapl:WearablesHomeandAccessoriesMember', 'label': 'Wearables', 'type': 'Product or Service'}]
                    }
                ]
            }
        ],
        'income_statements': [
            {
                'ticker': 'AAPL',
                'report_period': '2024-09-28',
                'revenue': 391035000000.0,
                'gross_profit': 180683000000.0,
                'research_and_development': 31370000000.0,
                'operating_income': 123216000000.0
            }
        ]
    },
    'MSFT': {
        'name': 'Microsoft Corporation',
        'segmented_revenues': [
            {
                'ticker': 'MSFT',
                'period': 'annual',
                'report_period': '2024-06-30',
                'items': [
                    {
                        'name': 'Revenue',
                        'amount': 65585000000.0,
                        'segments': [{'key': 'msft:ProductivityAndBusinessProcessesMember', 'label': 'Productivity and Business Processes', 'type': 'Statement Business Segments'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 111598000000.0,
                        'segments': [{'key': 'msft:IntelligentCloudMember', 'label': 'Intelligent Cloud', 'type': 'Statement Business Segments'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 59655000000.0,
                        'segments': [{'key': 'msft:MorePersonalComputingMember', 'label': 'More Personal Computing', 'type': 'Statement Business Segments'}]
                    }
                ]
            }
        ],
        'income_statements': [
            {
                'ticker': 'MSFT',
                'report_period': '2024-06-30',
                'revenue': 245122000000.0,
                'gross_profit': 171450000000.0,
                'research_and_development': 27195000000.0,
                'operating_income': 109430000000.0
            }
        ]
    },
    'QCOM': {
        'name': 'QUALCOMM Incorporated',
        'segmented_revenues': [
            {
                'ticker': 'QCOM',
                'period': 'annual',
                'report_period': '2024-09-29',
                'items': [
                    {
                        'name': 'Revenue',
                        'amount': 28037000000.0,
                        'segments': [{'key': 'qcom:QCTMember', 'label': 'QCT', 'type': 'Statement Business Segments'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 8411000000.0,
                        'segments': [{'key': 'qcom:QTLMember', 'label': 'QTL', 'type': 'Statement Business Segments'}]
                    }
                ]
            }
        ],
        'income_statements': [
            {
                'ticker': 'QCOM',
                'report_period': '2024-09-29',
                'revenue': 38963000000.0,
                'gross_profit': 22384000000.0,
                'research_and_development': 8033000000.0,
                'operating_income': 11083000000.0
            }
        ]
    },
    'NVDA': {
        'name': 'NVIDIA Corporation',
        'segmented_revenues': [
            {
                'ticker': 'NVDA',
                'period': 'annual',
                'report_period': '2024-01-28',
                'items': [
                    {
                        'name': 'Revenue',
                        'amount': 47523000000.0,
                        'segments': [{'key': 'nvda:ComputeAndNetworkingMember', 'label': 'Compute and Networking', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 12488000000.0,
                        'segments': [{'key': 'nvda:GraphicsMember', 'label': 'Graphics', 'type': 'Product or Service'}]
                    }
                ]
            }
        ],
        'income_statements': [
            {
                'ticker': 'NVDA',
                'report_period': '2024-01-28',
                'revenue': 60922000000.0,
                'gross_profit': 45365000000.0,
                'research_and_development': 8675000000.0,
                'operating_income': 32972000000.0
            }
        ]
    },
    'TSLA': {
        'name': 'Tesla, Inc.',
        'segmented_revenues': [
            {
                'ticker': 'TSLA',
                'period': 'annual',
                'report_period': '2023-12-31',
                'items': [
                    {
                        'name': 'Revenue',
                        'amount': 82419000000.0,
                        'segments': [{'key': 'tsla:AutomotiveSalesMember', 'label': 'Automotive Sales', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 6037000000.0,
                        'segments': [{'key': 'tsla:EnergyGenerationAndStorageMember', 'label': 'Energy Generation and Storage', 'type': 'Product or Service'}]
                    },
                    {
                        'name': 'Revenue',
                        'amount': 8161000000.0,
                        'segments': [{'key': 'tsla:ServicesAndOtherMember', 'label': 'Services and Other', 'type': 'Product or Service'}]
                    }
                ]
            }
        ],
        'income_statements': [
            {
                'ticker': 'TSLA',
                'report_period': '2023-12-31',
                'revenue': 96773000000.0,
                'gross_profit': 17660000000.0,
                'research_and_development': 3969000000.0,
                'operating_income': 8891000000.0
            }
        ]
    }
}

def get_demo_data(ticker: str):
    """Get demo data for a ticker"""
    return DEMO_COMPANIES.get(ticker.upper(), None)

def is_demo_mode_available(ticker: str) -> bool:
    """Check if demo data is available for a ticker"""
    return ticker.upper() in DEMO_COMPANIES

def get_available_demo_tickers():
    """Get list of tickers with demo data"""
    return list(DEMO_COMPANIES.keys())
