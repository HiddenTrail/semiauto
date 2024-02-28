*** Settings ***
Library                   Browser
Library                   libs${/}ImageSimilarityLibrary.py

Suite Teardown            Close Browser    ALL

*** Variables ***
${CONSENT_BUTTON}         //p[@class="fc-button-label"][text()="Consent"]
${UPLOAD_IMAGE_INPUT}     //input[@type="file"]
${UPLOAD_COMPLETED}       //h2[text()="Upload completed!"]
${IMAGE_LINK}             //div[@class="row"][.//div[text()="Direct link:"]]//input
${IMAGE_SOURCE}           upload${/}kekkonen.jpg
${EXPECTED_IMAGE}         expected${/}kekkonen1977.jpg
${NOT_EXPECTED_IMAGE}     expected${/}ritariassa.jpg


*** Test Cases ***
Kekkonen is expectedly Kekkonen
    New Browser                      chromium    headless=No
    New Page                         https://postimages.org/
    Click away consent
    Upload File By Selector          ${UPLOAD_IMAGE_INPUT}    ${IMAGE_SOURCE}
    Wait Until Upload Completes
    ${linked_image_url}=             Get Text    ${IMAGE_LINK}
    Assert Images Are Similar        ${EXPECTED_IMAGE}   ${linked_image_url}

Kekkonen is not Knight Rider
    New Browser                      chromium    headless=No
    New Page                         https://postimages.org/
    Click away consent
    Upload File By Selector          ${UPLOAD_IMAGE_INPUT}    ${IMAGE_SOURCE}
    Wait Until Upload Completes
    ${linked_image_url}=             Get Text    ${IMAGE_LINK}
    Assert Images Are Not Similar    ${NOT_EXPECTED_IMAGE}   ${linked_image_url}

*** Keywords ***
Click away consent
    ${button_exists} =    Get Element States    ${CONSENT_BUTTON}    then    bool(value & visible)  # Returns ${True} if element is visible
    Run Keyword If    ${button_exists}    Click    ${CONSENT_BUTTON}

Wait Until Upload Completes
    Wait For Elements State    ${UPLOAD_COMPLETED}    visible    timeout=30s
