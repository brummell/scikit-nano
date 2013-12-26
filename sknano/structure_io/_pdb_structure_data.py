# -*- coding: utf-8 -*-
"""
==============================================================================
PDB format (:mod:`sknano.structure_io._pdb_structure_data`)
==============================================================================

.. currentmodule:: sknano.structure_io._pdb_structure_data

"""
from __future__ import division, print_function, absolute_import

__docformat__ = 'restructuredtext'

from pksci.chemistry import Atom
from pkshared.tools.fiofuncs import get_fpath

from ._structure_data import StructureReader, StructureReaderError, \
    StructureWriter


__all__ = ['PDBDATA', 'PDBReader', 'PDBWriter']


class PDBReader(StructureReader):
    """Class for reading pdb chemical file format.

    Parameters
    ----------
    pdbfile : str
        pdb structure file

    """
    def __init__(self, fname=None):
        super(PDBReader, self).__init__(fname=fname)
        self._read()

    def _read(self):
        with open(self._fname, 'r') as f:
            self._Natoms = int(f.readline().strip())
            self._comment_line = f.readline().strip()
            lines = f.readlines()
            for line in lines:
                s = line.strip().split()
                if len(s) != 0:
                    atom = \
                        Atom(s[0], x=float(s[1]), y=float(s[2]), z=float(s[3]))
                    self._atoms.append(atom)


class PDBWriter(StructureWriter):
    """Class for writing pdb chemical file format."""

    @classmethod
    def write(cls, fname=None, atoms=None, comment_line=None):
        """Write structure data to file.

        Parameters
        ----------
        fname : str
        atoms : Atoms
            :py:class:`~pksci.chemistry.Atoms` instance.
        comment_line : str, optional

        """
        if fname is None:
            raise TypeError('fname argument must be a string!')
        elif atoms is None:
            raise TypeError('atoms argument must be an Atoms object')
        else:
            fname = get_fpath(fname=fname, ext='pdb', overwrite=True)
            if comment_line is None:
                comment_line = fname

            atoms.fix_minus_zero_coords()

            with open(fname, 'w') as f:
                f.write('{:d}\n'.format(atoms.Natoms))
                f.write('{}\n'.format(comment_line))
                for atom in atoms:
                    f.write('{:3s} {:10.5f} {:10.5f} {:10.5f}\n'.format(
                        atom.symbol, atom.x, atom.y, atom.z))


class PDBDATA(PDBReader):
    """Class for reading and writing structure data in PDB data format.

    Parameters
    ----------
    fname : str, optional

    """
    def __init__(self, fname=None):
        try:
            super(PDBDATA, self).__init__(fname=fname)
        except StructureReaderError:
            pass

    def write(self, pdbfile=None):
        if pdbfile is None:
            pdbfile = self._fname
        PDBWriter.write(fname=pdbfile, atoms=self._atoms,
                        comment_line=self._comment_line)