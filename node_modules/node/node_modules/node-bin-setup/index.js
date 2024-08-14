var spawn = require('child_process').spawn;
var path = require('path');
var fs = require('fs');

function installArchSpecificPackage(version, require) {

  process.env.npm_config_global = 'false';

  var platform = process.platform == 'win32' ? 'win' : process.platform;
  var arch = platform == 'win' && process.arch == 'ia32' ? 'x86' : process.arch;
  var prefix = (process.platform == 'darwin' && process.arch == 'arm64') ? 'node-bin' : 'node';

  var cp = spawn(platform == 'win' ? 'npm.cmd' : 'npm', ['install', '--no-save', [prefix, platform, arch].join('-') + '@' + version], {
    stdio: 'inherit',
    shell: true
  });

  cp.on('close', function(code) {
    var pkgJson = require.resolve([prefix, platform, arch].join('-') + '/package.json');
    var subpkg = JSON.parse(fs.readFileSync(pkgJson, 'utf8'));
    var executable = subpkg.bin.node;
    var bin = path.resolve(path.dirname(pkgJson), executable);

    try {
      fs.mkdirSync(path.resolve(process.cwd(), 'bin'));
    } catch (e) {
      if (e.code != 'EEXIST') {
        throw e;
      }
    }

    linkSync(bin, path.resolve(process.cwd(), executable));

    if (platform == 'win') {
      var pkg = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'package.json')));
      fs.writeFileSync(path.resolve(process.cwd(), 'bin/node'), 'This file intentionally left blank');
      pkg.bin.node = 'bin/node.exe';
      fs.writeFileSync(path.resolve(process.cwd(), 'package.json'), JSON.stringify(pkg, null, 2));
    }

    return process.exit(code);

  });
}

function linkSync(src, dest) {
  try {
    fs.unlinkSync(dest);
  } catch (e) {
    if (e.code != 'ENOENT') {
      throw e;
    }
  }
  return fs.linkSync(src, dest);
}

module.exports = installArchSpecificPackage;
