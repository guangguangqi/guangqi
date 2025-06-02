from openmm.app import PDBFixer
from openmm.app import Modeller
from openmm.app import ForceField
from openmm.app import PDBFile
from openmm.app import Simulation
from openmm import LangevinIntegrator
from openmm import unit
from sys import stdout

# 加载并修复 PDB 文件
fixer = PDBFixer(filename='protein_ligand.pdb')
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(pH=7.0)

# 保存修复后的 PDB 文件
with open('fixed_protein_ligand.pdb', 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)
