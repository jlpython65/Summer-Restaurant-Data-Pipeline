from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import google.auth


def sheets_batch_update(spreadsheet_id, title, find, replacement):
  """
  Update the sheet details in batch, the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  creds, _ = google.auth.default()
  # pylint: disable=maybe-no-member

  try:
    service = build("sheets", "v4", credentials=creds)

    requests = []
    # Change the spreadsheet's title.
    requests.append(
        {
            "updateSpreadsheetProperties": {
                "properties": {"title": title},
                "fields": "title",
            }
        }
    )
    # Find and replace text
    requests.append(
        {
            "findReplace": {
                "find": find,
                "replacement": replacement,  
                "allSheets": True,
            }
        }
    )
    # Add additional requests (operations) ...

    body = {"requests": requests}
    response = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
    find_replace_response = response.get("replies")[1].get("findReplace")
    print(
        f"{find_replace_response.get('occurrencesChanged')} replacements made."
    )
    return response

  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
  sheets_batch_update("spreadsheet_id", "title", "find", "replacement")