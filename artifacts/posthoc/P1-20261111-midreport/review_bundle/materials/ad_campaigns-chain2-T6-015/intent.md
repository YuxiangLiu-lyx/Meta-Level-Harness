# Advertising Campaigns — Budget Approval then Launch

## Natural-Language Scenario

The system manages advertising campaigns and their creatives in a marketing platform.

The people involved are advertisers, account managers, brand safety reviewers, and campaign directors. One person may hold both the account-manager and the campaign-director role at the same time.

The resources are campaigns and creatives. Every campaign records its advertiser, who prepared it, its budget, its contingency, its budget tier, its risk labels, its scheduled start, and its status.

Each request carries the current time, whether multi-factor authentication was used, whether the device is trusted, and whether an emergency launch is declared.

In this workflow a campaign's budget is first approved and then the campaign is launched, and the launch step can see the campaign's status and who prepared it as recorded by the approval step.

An account manager or campaign director who prepared a campaign may not approve its budget when its budget plus contingency crosses the threshold, and for a budget plus contingency at or below the threshold the preparer may approve it.

A budget may be approved only when multi-factor authentication was used, and a request to approve one without multi-factor authentication is refused.

A campaign may be launched only after its budget has been approved, and a request to launch one whose budget is not yet approved is refused.

A campaign may be launched only by its owning advertiser, and an account manager or campaign director who is not the owning advertiser may not launch it.

A campaign may be launched only when it carries the required risk label, and a request to launch one without that label is refused.

A run through the workflow in which a campaign director who did not prepare a campaign approves its budget with multi-factor authentication and the owning advertiser then launches the campaign carrying the required risk label, tripping no prohibition above, must be able to succeed.
