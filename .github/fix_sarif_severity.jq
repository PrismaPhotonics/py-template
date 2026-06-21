# jq script to fix SARIF security-severity for GitHub compatibility
# This script converts confidence levels in tags to numerical security-severity values
#
# Mapping:
# - HIGH CONFIDENCE -> 9.0 (Critical/High severity)
# - MEDIUM CONFIDENCE -> 5.0 (Medium severity)
# - LOW CONFIDENCE -> 1.0 (Low severity)
# - No confidence tag -> 3.0 (Default medium-low severity)

def extract_confidence_and_map_severity:
  # Extract confidence level from tags and map to numerical severity as string (GitHub requirement)
  (.properties.tags // []) as $tags |
  if ($tags | any(. == "HIGH CONFIDENCE")) then "9.0"
  elif ($tags | any(. == "MEDIUM CONFIDENCE")) then "5.0"
  elif ($tags | any(. == "LOW CONFIDENCE")) then "1.0"
  else "3.0"  # default for cases without explicit confidence
  end;

# Walk through the SARIF structure and add security-severity to rules
walk(
  if type == "object" and has("rules") then
    .rules |= map(
      if has("properties") then
        .properties."security-severity" = extract_confidence_and_map_severity
      else
        .properties = {"security-severity": extract_confidence_and_map_severity}
      end
    )
  else
    .
  end
)
