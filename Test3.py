from CheckmarxPythonSDK.CxOne import scannersResultsAPI, scaManagementOfRiskAPI
from CheckmarxPythonSDK.CxOne.dto import SupplyChainRiskAction
from CheckmarxPythonSDK.CxOne.scaManagementOfRiskAPI import (
    UpdateVulnerabilitiesBulkRequest,
    UpdateVulnerabilityRequest,
)

# ---- inputs ----
PROJECT_ID = "7d56df75-29ec-4e81-bfa3-21be6e8951ba"
SCAN_ID = "ef23ae99-7205-4677-b5c1-e6afd037c1e4"
SEVERITIES = ["HIGH", "CRITICAL"]      # add "MEDIUM" if you want those too
COMMENT = "Confirmed after security review"
DRY_RUN = True                         # set False to actually apply


def split_package(identifier):
    """'Npm-jquery-1.4.2' -> ('Npm', 'jquery', '1.4.2')"""
    manager, rest = identifier.split("-", 1)
    name, version = rest.rsplit("-", 1)
    return manager, name, version


def fetch_sca(scan_id):
    out, offset = [], 0
    while True:
        r = scannersResultsAPI.get_all_scanners_results_by_scan_id(
            scan_id=scan_id, offset=offset, limit=100)
        rs = r["results"] if isinstance(r, dict) else r.results
        out += [x for x in rs if str(getattr(x, "type", "")).lower() == "sca"]
        if len(rs) < 100:
            return out
        offset += 100


def confirm(results):
    entries = []
    for r in results:
        manager, name, version = split_package(r.data["packageIdentifier"])
        entries.append(UpdateVulnerabilityRequest(
            packageName=name,
            packageVersion=version,
            packageManager=manager,
            vulnerabilityId=r.id,
            projectIds=[PROJECT_ID],
            actions=[SupplyChainRiskAction(
                actionType="ChangeState", value="Confirmed", comment=COMMENT)],
        ))
    resp = scaManagementOfRiskAPI.update_vulnerabilities_bulk(
        UpdateVulnerabilitiesBulkRequest(packageVulnerabilitiesProfile=entries))
    print(resp)


if __name__ == "__main__":
    results = fetch_sca(SCAN_ID)
    targets = [r for r in results
               if r.severity in SEVERITIES and r.state != "CONFIRMED"]
    print(f"{len(results)} SCA results, {len(targets)} to confirm "
          f"({', '.join(SEVERITIES)})")
    for r in targets:
        print(f"  {r.severity:8} {r.id:20} {r.data['packageIdentifier']}")
    if targets and not DRY_RUN:
        confirm(targets)
    elif targets:
        print("DRY_RUN is True - nothing changed. Set DRY_RUN = False to apply.")
