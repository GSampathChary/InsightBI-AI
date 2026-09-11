import os
import httpx

def test_upload_api():
    csv_data = (
        "order_id,date,customer_id,product_id,product_name,category,quantity,unit_price,unit_cost,discount,region_name\n"
        "ORD-9901,2024-05-01,1,101,Enterprise Laptop Pro,Technology,10,1200.00,800.00,0.0,North America East\n"
        "ORD-9902,2024-05-02,2,105,Cloud License Enterprise,Software,50,200.00,40.00,0.1,North America West\n"
        "ORD-9903,2024-05-03,3,103,Ergonomic Office Chair,Furniture,20,350.00,200.00,0.05,South Region\n"
    )

    files = {'file': ('test_sales.csv', csv_data.encode('utf-8'), 'text/csv')}

    print("Uploading test sales CSV to http://127.0.0.1:8000/api/v1/upload/csv...")
    response = httpx.post("http://127.0.0.1:8000/api/v1/upload/csv", files=files, timeout=10.0)

    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(response.json())

    assert response.status_code == 200, "Upload failed"
    assert response.json().get("success") is True, "Expected success=True"
    print("✅ CSV Upload API Test Passed!")

if __name__ == "__main__":
    test_upload_api()
