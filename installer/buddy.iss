#define MyAppName "Buddy"
#ifndef MyAppVersion
  #define MyAppVersion "0.1.0"
#endif

[Setup]
AppId={{B1B1A4EE-24C4-4AAE-8E13-63272701562D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=is-leeroy-jenkins
DefaultDirName={localappdata}\Programs\Buddy
DefaultGroupName=Buddy
OutputDir=..\dist-installer
OutputBaseFilename=Buddy-Setup-{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
WizardStyle=modern
UninstallDisplayName=Buddy
UninstallDisplayIcon={app}\Buddy.exe
CloseApplications=yes

[Files]
Source: "..\dist\Buddy\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Icons]
Name: "{group}\Buddy"; Filename: "{app}\Buddy.exe"
Name: "{autodesktop}\Buddy"; Filename: "{app}\Buddy.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Buddy.exe"; Description: "Launch Buddy"; Flags: nowait postinstall skipifsilent
