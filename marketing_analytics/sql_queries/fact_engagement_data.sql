-- Restructuring ID columns to come first
-- Creating a uniform format for the ContentType column
-- Changing the date format of EngagementDate to 'dd.MM.yyyy'
-- Separating Views and Clicks from ViewsClicksCombined
-- Excluding 'Newsletter' from ContentType as it is not Digital Media

SELECT 
    EngagementID,
    ContentID,
    CampaignID,
    ProductID,
    UPPER(REPLACE(ContentType, 'Socialmedia', 'Social Media')) AS ContentType,
    LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,
    Likes,
    FORMAT(CONVERT(DATE, EngagementDate), 'dd.MM.yyyy') AS EngagementDate
FROM 
    dbo.engagement_data
WHERE 
    ContentType != 'Newsletter';
