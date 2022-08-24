-- ****************************************************
-- *                       seps                       *
-- ****************************************************
CREATE TABLE IF NOT EXISTS seps (
   SepName VARCHAR(60) PRIMARY KEY NOT NULL,
   EVI     INT NOT NULL CHECK(EVI > 50000) UNIQUE
);


-- ****************************************************
-- *                       sites                      *
-- ****************************************************
CREATE TABLE IF NOT EXISTS sites (
   SiteID      INT PRIMARY KEY NOT NULL,
   SiteName    VARCHAR NOT NULL,
   SiteAddress TEXT,
   Etc         TEXT
);


-- ****************************************************
-- *                       vrfs                       *
-- ****************************************************
CREATE TABLE IF NOT EXISTS vrfs (
   VRFName           VARCHAR(60) PRIMARY KEY NOT NULL,
   RouteTargetImport VARCHAR(60) NOT NULL
);


-- ****************************************************
-- *                      routers                     *
-- ****************************************************
CREATE TABLE IF NOT EXISTS routers (
   RouterName VARCHAR(60) PRIMARY KEY NOT NULL,
   Loopback0  VARCHAR(20) NOT NULL UNIQUE,
   Model      VARCHAR,
   Role       VARCHAR,
   ASNumber   INT NOT NULL,
   SiteID     INT NOT NULL,
   FOREIGN KEY (SiteID)
    REFERENCES sites(SiteID)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);


-- ****************************************************
-- *                       ports                      *
-- ****************************************************
CREATE TABLE IF NOT EXISTS ports (
   id         INT PRIMARY KEY NOT NULL,
   RouterName VARCHAR(60) NOT NULL,
   PortName   VARCHAR(60) NOT NULL,
   FOREIGN KEY (RouterName)
    REFERENCES routers(RouterName)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);


-- ****************************************************
-- *                     SepPortRelation              *
-- ****************************************************
CREATE TABLE IF NOT EXISTS SepPortRelation (
   id           INT PRIMARY KEY NOT NULL,
   SepName      VARCHAR NOT NULL,
   RouterPortID INT NOT NULL,
   FOREIGN KEY (RouterPortID)
    REFERENCES ports(id)
      ON DELETE RESTRICT 
      ON UPDATE CASCADE,
   FOREIGN KEY (SepName)
    REFERENCES seps(SepName)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);


-- ****************************************************
-- *                        IPs                       *
-- ****************************************************
CREATE TABLE IF NOT EXISTS IPs (
   IP           VARCHAR(20) PRIMARY KEY NOT NULL,
   MAC          VARCHAR(20) NOT NULL,
   RouterPortID INT,
   VLAN         INT NOT NULL,
   VRFName      VARCHAR NOT NULL,
   UpdatedOn	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (RouterPortID)
    REFERENCES ports(id)
      ON DELETE SET NULL
      ON UPDATE CASCADE,
   FOREIGN KEY (VRFName)
    REFERENCES vrfs(VRFName)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

