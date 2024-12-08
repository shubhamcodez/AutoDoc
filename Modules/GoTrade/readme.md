###  Instructions to Run Exchange Example Scripts

This README provides detailed instructions for running the exchange example scripts and configuring them as per your requirements.

---

### **Overview**

These Python scripts demonstrate how to interact with different cryptocurrency exchanges using the OEMS (Order Execution Management System). They allow you to:
- Log in to an exchange.
- Place orders (Market, Limit, TWAP, Market Edge, TWAP Edge).

The examples include:
1. `okx-examples.py`
2. `deribit-example.py`
3. `binance-usdm-exmaple.py`
4. `binance-spot-example.py`
5. `binance-coinm-exmaple.py`
6. `bybit-example.py`

---

### **Prerequisites**

1. **Python**:
   - Ensure Python 3.6+ is installed on your system.
   - Verify installation: `python3 --version`.

2. **Required Libraries**:
   - Install dependencies via `pip`:
     ```bash
     pip install requests
     ```

3. **API Keys and Secrets**:
   - Obtain API keys and secrets from the respective exchange dashboards.
   - Replace placeholders (`key`, `secret`) in the scripts with your actual credentials.

4. **Directory Setup**:
   - Ensure the `oems_operations.py` file and other dependencies are available in the parent directory of these scripts.

---

### **How to Run a Script**

1. **Select the Exchange**:
   - Use the script corresponding to the exchange you want to interact with (e.g., `deribit-example.py` for Deribit).

2. **Update Configuration**:
   - Modify the following placeholders in the `main` function of the script:
     - `account_name`: Replace with your exchange account name.
     - `key`: Replace with your API key.
     - `secret`: Replace with your API secret.
     - `symbol`: Update with the symbol for the asset you want to trade (e.g., `BTCUSDT`).

   Example (`deribit-example.py`):
   ```python
   if not login(
       exchange_name="deribit",
       account_name="your_account_name",
       key="your_api_key",
       secret="your_api_secret"
   ):
       print("Login failed")
       return
   ```

3. **Execute the Script**:
   - Run the script from the terminal:
     ```bash
     python3 deribit-example.py
     ```

4. **Output**:
   - The script will display responses for login and order placements in the terminal.

---

### **Configuration Parameters**

| **Parameter**      | **Description**                                                | **Example**       |
|---------------------|----------------------------------------------------------------|-------------------|
| `exchange_name`     | The name of the exchange.                                      | `"deribit"`       |
| `account_name`      | Your account identifier on the exchange.                      | `"test_account"`  |
| `key`               | API key for the exchange.                                     | `"your_api_key"`  |
| `secret`            | API secret for the exchange.                                  | `"your_api_secret"` |
| `symbol`            | Trading pair or symbol.                                       | `"BTC-PERPETUAL"` |
| `side`              | Order side (`buy` or `sell`).                                 | `"buy"`           |
| `quantity`          | Amount to trade.                                              | `0.1`             |
| `price`             | (For Limit Orders) Price to place the order.                  | `35000`           |
| `duration`          | (For TWAP/TWAP Edge) Total duration in seconds.               | `120`             |
| `interval`          | (For TWAP/TWAP Edge) Time interval between executions.        | `30`              |
| `max_timer`         | (For Market Edge) Time in seconds to execute the order.       | `30`              |

---

### **Exchange-Specific Configurations**

| **Exchange**       | **Script**                | **Example Configurations**                                    |
|---------------------|---------------------------|--------------------------------------------------------------|
| OKX                | `okx-examples.py`         | `exchange_name="okx", symbol="DOT-USDT-SWAP"`                |
| Deribit            | `deribit-example.py`      | `exchange_name="deribit", symbol="BTC-PERPETUAL"`            |
| Binance USDM       | `binance-usdm-exmaple.py` | `exchange_name="binanceusdm", symbol="EOSUSDT"`              |
| Binance Spot       | `binance-spot-example.py` | `exchange_name="binance", symbol="EOSUSDT"`                  |
| Binance COINM      | `binance-coinm-exmaple.py`| `exchange_name="binancecoinm", symbol="EOSUSDT"`             |
| Bybit              | `bybit-example.py`        | `exchange_name="bybit", symbol="EOSUSDT", instrument_type="LINEAR"` |

---

### **Key Notes**

1. **Instrument Type**:
   - **Only required for Bybit** (`instrument_type`).
   - Not needed for OKX, Deribit, or Binance.


2. **Order Types**:
   - Market, Limit, TWAP, Market Edge, and TWAP Edge are supported.

---

### **Troubleshooting**

- **Login Fails**:
  - Check if your API key and secret are correct.
  - Ensure the API is enabled for trading in your exchange account settings.


- **Invalid Symbol**:
  - Verify the trading pair exists on the exchange (e.g., `BTCUSDT` for Binance).

---
