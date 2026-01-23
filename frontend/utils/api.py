import streamlit as st
import requests
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime


class APIClient:
    """
    Enhanced API client for KPI Analyzer backend
    - Auto injects JWT token from Streamlit session
    - Centralized request + error handling
    """

    def __init__(self, base_url: Optional[str] = None):
        # Base URL
        if base_url is None:
            base_url = st.session_state.get(
                "api_url", "http://127.0.0.1:8000/api/v1"
            )

        self.base_url = base_url.rstrip("/")

        # Persistent HTTP session
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    # =========================
    # AUTH HEADER (AUTO)
    # =========================
    def _get_auth_headers(self) -> Dict[str, str]:
        token = st.session_state.get("token")
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    # =========================
    # CORE REQUEST HANDLER
    # =========================
    def _make_request(
        self,
        method: str,
        endpoint: str,
        raise_for_status: bool = True,
        **kwargs
    ) -> requests.Response:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # 1. Prepare additional headers (Auth + custom)
        extra_headers = kwargs.pop("headers", {})
        extra_headers.update(self._get_auth_headers())

        # 2. Handle File Uploads: Suppress session's default Content-Type
        if "files" in kwargs:
            extra_headers["Content-Type"] = None

        # 3. Handle JSON: Avoid passing json=None as it can trigger a body with "null"
        if "json" in kwargs and kwargs["json"] is None:
            kwargs.pop("json")

        # 4. Execute request
        response = self.session.request(
            method=method,
            url=url,
            headers=extra_headers,
            timeout=30,
            **kwargs
        )

        if raise_for_status:
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                # 🔥 Clean API error surfacing
                try:
                    detail = response.json()
                except Exception:
                    detail = response.text

                raise RuntimeError({
                    "status_code": response.status_code,
                    "error": detail
                }) from e

        return response

    # =========================
    # PUBLIC HTTP METHODS
    # =========================
    def get(self, endpoint: str, params: dict = None, raise_for_status: bool = True, **kwargs) -> requests.Response:
        return self._make_request(
            "GET", endpoint, params=params, raise_for_status=raise_for_status, **kwargs
        )

    def post(self, endpoint: str, json: dict = None, raise_for_status: bool = True, **kwargs) -> requests.Response:
        return self._make_request(
            "POST", endpoint, json=json, raise_for_status=raise_for_status, **kwargs
        )

    def delete(self, endpoint: str) -> bool:
        self._make_request("DELETE", endpoint)
        return True

    # =========================
    # KPI METHODS
    # =========================
    def get_kpis(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        business_units: List[str] = None,
        kpi_types: List[str] = None
    ) -> pd.DataFrame:

        params = {}

        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        if business_units:
            params["business_units"] = business_units
        if kpi_types:
            params["kpi_types"] = kpi_types

        response = self.get("kpis", params=params)
        data = response.json()

        df = pd.DataFrame(data)

        # Safe datetime parsing
        if "period" in df.columns:
            df["period"] = pd.to_datetime(df["period"], errors="coerce")
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

        return df

    def get_business_units(self) -> List[str]:
        response = self.get("business-units")
        data = response.json()
        return [bu["name"] for bu in data]


    def get_kpi_types(self) -> List[str]:
        response = self.get("kpis/types")
        data = response.json()
        return data.get("kpi_types", [])

    def calculate_kpi(
        self,
        kpi_type: str,
        period_start: datetime,
        period_end: datetime,
        business_units: List[str] = None
    ) -> Dict[str, Any]:

        payload = {
            "kpi_type": kpi_type,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat()
        }

        if business_units:
            payload["business_units"] = business_units

        response = self.post("kpis/calculate", json=payload)
        return response.json()
        
    def get_scheduled_reports(self) -> List[Dict[str, Any]]:
        """Get list of scheduled reports
        
        Returns:
            List of scheduled reports
        """
        response = self._make_request('GET', 'reports/scheduled')
        return response.json()

    def schedule_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a new report
        
        Args:
            report_config: Report configuration
            
        Returns:
            Dictionary with scheduled report details
        """
        response = self._make_request('POST', 'reports/schedule', json=report_config)
        return response.json()

    def delete_scheduled_report(self, report_id: str) -> Dict[str, Any]:
        """Delete a scheduled report
        
        Args:
            report_id: ID of the report to delete
            
        Returns:
            Dictionary with deletion result
        """
        response = self._make_request('DELETE', f'reports/scheduled/{report_id}')
        return response.json()

    def get_report_templates(self) -> List[Dict[str, Any]]:
        """Get available report templates
        
        Returns:
            List of report templates
        """
        response = self._make_request('GET', 'reports/templates')
        return response.json()

    def generate_report(self, report_config: Dict[str, Any], format: str = "excel") -> bytes:
        """Generate a report in specified format
        
        Args:
            report_config: Report configuration
            format: Export format (csv, excel, pdf)
            
        Returns:
            Report data as bytes
        """
        params = report_config.copy()
        
        if format == "csv":
            params['include_summary'] = report_config.get('include_summary', True)
            response = self._make_request('GET', 'reports/export/csv', params=params)
        elif format == "excel":
            params['include_charts'] = report_config.get('include_charts', True)
            response = self._make_request('GET', 'reports/export/excel', params=params)
        else:  # PDF
            params['template'] = report_config.get('template', 'standard')
            response = self._make_request('GET', 'reports/export/pdf', params=params)
        
        return response.content

# 🔥 DEBUG CONFIRMATION
print("🔥 utils.api v2 LOADED (with **kwargs) FROM:", __file__)
