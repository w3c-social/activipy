;;; Activipy --- ActivityStreams 2.0 implementation and testing for Python
;;; Copyright © 2015 Christopher Allan Webber
;;;
;;; This file is part of Activipy.
;;;
;;; Activipy is free software; you can redistribute it and/or modify it
;;; under the terms of the GNU General Public License as published by
;;; the Free Software Foundation; either version 3 of the License, or
;;; (at your option) any later version.
;;;
;;; Activipy is distributed in the hope that it will be useful, but
;;; WITHOUT ANY WARRANTY; without even the implied warranty of
;;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
;;; General Public License for more details.
;;;
;;; You should have received a copy of the GNU General Public License
;;; along with Activipy.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:
;;
;; Development environment for GNU Guix.
;;
;;; Code:

(use-modules (guix packages)
             (guix licenses)
             (guix build-system python)
             (gnu packages)
             (gnu packages python))

(package
  (name "activipy")
  (version "0.0")
  (source #f)
  (build-system python-build-system)
  (inputs
   `(("python" ,python)
     ("python-pyld" ,python-pyld)
     ("python-sphinx" ,python-sphinx)))
  (synopsis "ActivityStreams 2.0 implementation and testing for Python")
  (description "An ActivityStreams 2.0 implementation for Python.
Provides an easy API for building ActivityStreams 2.0 based applications
as well as a test suite for testing ActivityStreams 2.0 libraries against.")
  (home-page "TBD :)")
  ;; technically GPLv3+ or ASL2.0, which reduces to basically ASL2.0, but
  ;; maybe important if there are future compatibilities with later license
  ;; versions
  (license asl2.0))
