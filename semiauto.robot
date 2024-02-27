*** Settings ***
Library           Browser
Library           Dialogs

*** Variables ***
${CONSENT_BUTTON}           //p[@class="fc-button-label"][text()="Consent"]
${UPLOAD_IMAGE_BUTTON}      //span/i[contains(@class,"folder-open")]
${PROGRESS_BAR_SELECTOR}    //div[@class="progress"]
${IMAGE_LINK}               //div[@class="row"][.//div[text()="Link:"]]//input


*** Test Cases ***
Image upload and person recognition
    New Browser                     chromium    headless=No
    New Page                        https://postimages.org/
    Click away consent
    Pause Execution                 Select image file containing picture of president Kekkonen on OS specific file dialog
    Click                           ${UPLOAD_IMAGE_BUTTON}
    Wait Until Upload Completes
    ${linked_image}=                Get Text    ${IMAGE_LINK}
    New Page                        ${linked_image}
    Execute Manual Step             Does image represent president Kekkonen?

*** Keywords ***
Click away consent
    ${button_exists} =    Get Element States    ${CONSENT_BUTTON}    then    bool(value & visible)  # Returns ${True} if element is visible
    Run Keyword If    ${button_exists}    Click    ${CONSENT_BUTTON}

Wait Until Upload Completes
    Wait For Elements State    //h2[text()="Upload completed!"]    visible    timeout=30s

