#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const zlib = require('zlib');
const tar = require('tar');

const REPO = '477-Studio/claude-gym';
const BINARY_NAME = 'cgym';

function getPlatformInfo() {
  const platform = process.platform;
  const arch = process.arch;

  const platformMap = {
    darwin: 'darwin',
    linux: 'linux',
    win32: 'windows',
  };

  const archMap = {
    x64: 'amd64',
    arm64: 'arm64',
  };

  const os = platformMap[platform];
  const cpu = archMap[arch];

  if (!os || !cpu) {
    throw new Error(`Unsupported platform: ${platform}-${arch}`);
  }

  // Windows arm64 not supported
  if (os === 'windows' && cpu === 'arm64') {
    throw new Error('Windows ARM64 is not supported yet');
  }

  // Linux arm64 not supported yet
  if (os === 'linux' && cpu === 'arm64') {
    throw new Error('Linux ARM64 is not supported yet');
  }

  return { os, cpu, isWindows: platform === 'win32' };
}

function getAssetName(version, os, cpu) {
  const ext = os === 'windows' ? 'zip' : 'tar.gz';
  return `claude-gym_${version}_${os}_${cpu}.${ext}`;
}

function getPackageVersion() {
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8'));
  return pkg.version;
}

async function getReleaseByTag(tag) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${REPO}/releases/tags/${tag}`,
      headers: {
        'User-Agent': 'claude-gym-npm-installer',
      },
    };

    https.get(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destPath);

    const request = (url) => {
      https.get(url, {
        headers: { 'User-Agent': 'claude-gym-npm-installer' }
      }, (response) => {
        if (response.statusCode === 302 || response.statusCode === 301) {
          request(response.headers.location);
          return;
        }

        if (response.statusCode !== 200) {
          reject(new Error(`Failed to download: ${response.statusCode}`));
          return;
        }

        response.pipe(file);
        file.on('finish', () => {
          file.close(resolve);
        });
      }).on('error', (err) => {
        fs.unlink(destPath, () => {});
        reject(err);
      });
    };

    request(url);
  });
}

async function extractTarGz(archivePath, destDir, binaryName) {
  return new Promise((resolve, reject) => {
    fs.createReadStream(archivePath)
      .pipe(zlib.createGunzip())
      .pipe(tar.extract({ cwd: destDir }))
      .on('finish', resolve)
      .on('error', reject);
  });
}

async function extractZip(archivePath, destDir) {
  // Use system unzip on Unix, PowerShell on Windows
  if (process.platform === 'win32') {
    execSync(`powershell -command "Expand-Archive -Path '${archivePath}' -DestinationPath '${destDir}' -Force"`);
  } else {
    execSync(`unzip -o "${archivePath}" -d "${destDir}"`);
  }
}

async function main() {
  try {
    console.log('Installing Claude Gym...');

    const { os, cpu, isWindows } = getPlatformInfo();
    console.log(`Platform: ${os}-${cpu}`);

    // Get release matching package.json version
    const pkgVersion = getPackageVersion();
    const tag = `v${pkgVersion}`;
    console.log(`Version: ${tag}`);
    const release = await getReleaseByTag(tag);
    const version = release.tag_name;

    // Find the right asset
    const assetName = getAssetName(version, os, cpu);
    const asset = release.assets.find((a) => a.name === assetName);

    if (!asset) {
      throw new Error(`Could not find release asset: ${assetName}`);
    }

    // Download
    const binDir = path.join(__dirname, '..', 'bin');
    const tmpDir = path.join(__dirname, '..', '.tmp');

    if (!fs.existsSync(binDir)) fs.mkdirSync(binDir, { recursive: true });
    if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

    const archivePath = path.join(tmpDir, assetName);
    console.log(`Downloading ${assetName}...`);
    await downloadFile(asset.browser_download_url, archivePath);

    // Extract
    console.log('Extracting...');
    if (isWindows) {
      await extractZip(archivePath, tmpDir);
      fs.renameSync(
        path.join(tmpDir, `cgym-windows-amd64.exe`),
        path.join(binDir, 'cgym.exe')
      );
    } else {
      await extractTarGz(archivePath, tmpDir);
      const extractedBinary = path.join(tmpDir, `cgym-${os}-${cpu}`);
      const destBinary = path.join(binDir, BINARY_NAME);
      fs.renameSync(extractedBinary, destBinary);
      fs.chmodSync(destBinary, '755');
    }

    // Cleanup
    fs.rmSync(tmpDir, { recursive: true, force: true });

    console.log('Claude Gym installed successfully!');
    console.log('Run "cgym" to watch your current project.');
  } catch (error) {
    console.error('Installation failed:', error.message);
    process.exit(1);
  }
}

main();
