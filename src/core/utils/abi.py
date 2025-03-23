# ----------------------- Active Pool -----------------------
activePool = [
    {
        "inputs": [],
        "name": "getCollBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getBoldDebt",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ----------------------- Price Feed -----------------------
priceFeed = [
    {
        "inputs": [],
        "name": "lastGoodPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# --------------------- Stability Pool ---------------------
stabilityPool = [
    {
        "inputs": [],
        "name": "getTotalBoldDeposits",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ---------------------- Sorted Trove ----------------------
sortedTrove = [
    {
      "inputs": [],
      "name": "getSize",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "troveManager",
      "outputs": [
        {
          "internalType": "contract ITroveManager",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
]

# ---------------------- Trove Manager ---------------------
troveManager = [
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_index",
        "type": "uint256"
      }
    ],
    "name": "getTroveFromTroveIdsArray",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_troveId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_price",
        "type": "uint256"
      }
    ],
    "name": "getCurrentICR",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_troveId",
        "type": "uint256"
      }
    ],
    "name": "getLatestTroveData",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "entireDebt",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "entireColl",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "redistBoldDebtGain",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "redistCollGain",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accruedInterest",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "recordedDebt",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "annualInterestRate",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "weightedRecordedDebt",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "accruedBatchManagementFee",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "lastInterestRateAdjTime",
            "type": "uint256"
          }
        ],
        "internalType": "struct LatestTroveData",
        "name": "trove",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "troveNFT",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

# ------------------------ Trove NFT -----------------------
troveNFT = [
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "ownerOf",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
]