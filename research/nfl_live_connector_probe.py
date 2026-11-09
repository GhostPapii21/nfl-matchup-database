"""Opt-in NFL provider access check. Never stores keys or API response bodies."""
import importlib.util,json,os
from datetime import datetime,timezone
from pathlib import Path
from source_adapters.nfl_external_sources import fetch_http

def probe():
    result={"sport":"NFL","as_of_utc":datetime.now(timezone.utc).isoformat(),
            "production_ingest_enabled":False,"responses_saved":False,"sources":{}}
    for provider,key_name,params in (
        ("balldontlie_nfl","NFL_BDL_API_KEY",{"season":2026,"week":9}),
        ("api_sports_nfl","NFL_API_SPORTS_KEY",{"season":2026}),
    ):
        token=os.environ.get(key_name)
        if not token:
            result["sources"][provider]={"status":"CREDENTIAL_NOT_CONFIGURED",
                                          "secret_env_name":key_name}
            continue
        try:
            evidence=fetch_http(provider,"games",enabled=True,
                                key=token,params=params)
            response=evidence["data"]
            if not isinstance(response,dict):
                status="UNEXPECTED_RESPONSE_SCHEMA"
            elif response.get("errors") or response.get("error"):
                status="PROVIDER_RETURNED_ERROR"
            elif (provider=="balldontlie_nfl" and
                  not isinstance(response.get("data"),list)) or (
                  provider=="api_sports_nfl" and
                  not isinstance(response.get("response"),list)):
                status="UNEXPECTED_RESPONSE_SCHEMA"
            else:
                status="RESPONSE_RECEIVED_NEEDS_ID_AND_LICENSE_AUDIT"
            result["sources"][provider]={
                "status":status,"resource":"games","source_url":evidence["source_url"],
                "response_retrieved_at_utc":evidence["retrieved_at_utc"],
                "data_as_of_utc":None,"payload_stored":False}
        except Exception as exc:
            result["sources"][provider]={
                "status":"UNAVAILABLE_OR_REQUEST_FAILED",
                "error_class":type(exc).__name__,"payload_stored":False}
    result["sources"]["sportsdataverse_nfl"]={
        "status":"OPTIONAL_PACKAGE_NOT_ENABLED_AS_LIVE_LOADER",
        "package_manifest":"requirements-nfl-external-research.txt"}
    result["sources"]["cloudbet_nfl_mcp"]={
        "status":"DISABLED_CANDIDATE_UNVERIFIED_NOT_INGESTED"}
    return result

def main():
    report=probe()
    target=Path("research/NFL_LIVE_CONNECTOR_STATUS_20261109.json")
    target.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("NFL_CONNECTOR_STATUS=",json.dumps(
          {k:v["status"] for k,v in report["sources"].items()},sort_keys=True))

if __name__=="__main__":main()
