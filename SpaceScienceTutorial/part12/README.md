
=============================================================================
ROSETTA DSK Files
=============================================================================

  This "aareadme.txt" file describes the contents of the KERNELS/DSK
  directory of the ROSETTA SPICE data server. It also provides the file
  naming conventions used for the ROSETTA DSK kernels, and it provides
  identification of the most current version of each kind of DSK file.

  The contents of any DSK file may be easily determined using the
  'dskbrief' utility program, Example:

     % dskbrief <dsk_file_name>

  Descriptive information about how/why/when an DSK file was created
  is usually available in the 'comment area' of the file. This may be
  viewed using the 'commnt' utility program available in all copies of
  the SPICE Toolkit. Use the '-r' option to read the comments.
  Example:

     % commnt -r <dsk_file_name>

  All binary DSK files (*.BDS) contained in this directory are
  little-endian (LTL-IEEE) binary files.

  This DSK files have been produced by Nat Bachman NAIF/JPL
  (nathaniel.bachman@jpl.nasa.gov).

  Contact Marc Costa (mcosta@sciops.esa.int) or Dave Heather
  (dheather@rssd.esa.int) if you have any questions.


=============================================================================
References
=============================================================================
    1. Data Delivery Interface Document (DDID)       Appendix H - FD
       products Issue 3.0 (ROS-ESC-IF-5003)

    2. NAIF IDs Required Reading. NAIF Document No. 219.12  30 Jul 2003


=============================================================================
Rosetta DSK Directory Structure
=============================================================================
 aareadme.txt            Text file describing the directory structure,
                         the naming conventions for the DSKs, and the current
                         version(s) of each DSK type.

 former_versions         Subdirectory that contains obsolete versions of the
                         DSK files that have been updated in the Current DSK
                         Kernels Set.


=============================================================================
ROSETTA spacecraft DSK Naming Convention for the science phase:

                PPP_SC_STRUCT_Vvv.BDS

=============================================================================

         token          description
      ------------   --------------------------------------------
        PPP             project prefix: ROS

        SC              body: SC for Spacecraft, LR for Lander

        STRUCT          SC part: BUS (for the bus of spacecraft),
                        BUS_LR (for the bus of the spacecraft
                        with Philae), SAPY (for right Solar Array),
                        SAMY (for left Solar Array) or HGA.

        Vvv             version: V01, V02, V03 ....

        BDS             extension: .BDS


=============================================================================
ROSETTA main targets DSK Naming Convention for the science phase:

                PPP_BB_RRRR_IMETPRO_N_VV.BDS

=============================================================================

         token          description
      ------------   --------------------------------------------
        PPP             project prefix: ROS

        BB              body: CG for 67P/C-G, LU for Lutetia, or ST for Steins

        RRRR            number of plates: Knnn (for nnn thousand plates) or
                        Mnnn (for mmm million plates)

        IMETPRO         camera-method-producer combined into a single
                        7-character token:

                          I   -  camera:

                                 O for OSIRIS
                                 N for NAVCAM
                                 M for multiple

                          MET -  method:

                                 SPC for StereoPhotoClinometry
                                 MSD for Multi-Resolution StereoPhotoClinometry
                                 SPG for StereoPhotoGranulometry

                          PRO -  producer:

                                 ESA for European Space Agency/ESOC
                                 LAM for Laboratoire d'Astrophysique de Marseille
                                 LPS for Laboratoire d'Astrophysique de Marseille
                                         + Planetary Science Institute
                                 DLR for Deutsches Zentrum fur Luft- und
                                         Raumfahrt e.V.

        N              surface naming: U for unnamed (surface ID = body ID, for
                       use with Toolkits N0065 or earlier) or N for named
                       (surface IDs are set to distinct numbers that are mapped
                       to surface names using keywords provided in the project
                       FK v25 or later)

        VV             version: V1, V2, V3 ....

        BDS            extension: .BDS


=============================================================================
ROSETTA Generic Natural Bodies DSK Naming Covention:

                BODY_RRRR_PRO[_ID][_DESC]_vNN.bds

=============================================================================

         token          description
      ------------   --------------------------------------------
        BODY            body: TEMPEL1_9P for 9P/Tempel 1, PHOBOS for Phobos,
                        or DEIMOS for Deimos.

        RRRR            number of plates: Knnn (for nnn thousand plates) or
                        Mnnn (for mmm million plates)

        PRO             producer:

                           ESA for European Space Agency
                           DLR for Deutsches Zentrum fur Luft- und
                               Raumfahrt e.V.
                           GAS for Gaskell, R.W.
                           THO for Thomas, P.
                           MOL for Mars Global Surveyor MOLA data.


        NN              version: V01, V02, V03 ...

        BDS             extension: .BDS


=============================================================================
Current DSK Kernels Set
=============================================================================

 Name                              Comments
 --------------------------------  -------------------------------------
      ROS_CG_K006_OMSDLAM_N_V1.BDS
      ROS_CG_K012_OMSDLAM_N_V1.BDS
      ROS_CG_K024_OMSDLAM_N_V1.BDS
      ROS_CG_K048_OMSDLAM_N_V1.BDS
      ROS_CG_K098_OMSDLAM_N_V1.BDS
      ROS_CG_K191_OMSDLAM_N_V1.BDS
      ROS_CG_K391_OMSDLAM_N_V1.BDS
      ROS_CG_K760_OMSDLAM_N_V1.BDS
      ROS_CG_M001_OMSDLAM_N_V1.BDS  Contains 67P/C-G shape data based on
                                    OSIRIS images produced by LAM using
                                    MSPCD method with plate numbers
                                    from 6K to 1M, for use with
                                    Toolkits N0066 or later.

      ROS_CG_K006_OSPCLPS_N_V1.BDS
      ROS_CG_K012_OSPCLPS_N_V1.BDS
      ROS_CG_K024_OSPCLPS_N_V1.BDS
      ROS_CG_K050_OSPCLPS_N_V1.BDS
      ROS_CG_K096_OSPCLPS_N_V1.BDS
      ROS_CG_K195_OSPCLPS_N_V1.BDS
      ROS_CG_K399_OSPCLPS_N_V1.BDS
      ROS_CG_K786_OSPCLPS_N_V1.BDS  Contains 67P/C-G shape data based on
                                    OSIRIS images produced by LAM-PSI
                                    using SPC method with plate numbers
                                    from 6K to 3M, for use with
                                    Toolkits N0066 or later.

      ROS_CG_M004_NSPCESA_N_V1.BDS
      ROS_CG_K250_NSPCESA_N_V1.BDS
      ROS_CG_K104_NSPCESA_N_V1.BDS
      ROS_CG_M002_NSPCESA_N_V1.BDS  Contains 67P/C-G shape data based on
                                    NAVCAM images produced by ESA using
                                    SPC method with plate numbers from
                                    104K to 4M, for use with Toolkits
                                    N0066 or later.

      ROS_CG_K050_OSPGDLR_N_V1.BDS
      ROS_CG_K100_OSPGDLR_N_V1.BDS
      ROS_CG_K200_OSPGDLR_N_V1.BDS
      ROS_CG_M001_OSPGDLR_N_V1.BDS
      ROS_CG_M004_OSPGDLR_N_V1.BDS  Contains 67P/C-G shape data based on
                                    OSIRIS images produced by DLR using
                                    the SPG method with plate numbers
                                    from 50K to 4M, for use with
                                    Toolkits N0066 or later.

   Comet 67P/C-G DSKs, for use with Toolkit N0065 or earlier:

      ROS_CG_K006_OMSDLAM_U_V1.BDS
      ROS_CG_K012_OMSDLAM_U_V1.BDS
      ROS_CG_K024_OMSDLAM_U_V1.BDS
      ROS_CG_K048_OMSDLAM_U_V1.BDS
      ROS_CG_K098_OMSDLAM_U_V1.BDS
      ROS_CG_K191_OMSDLAM_U_V1.BDS
      ROS_CG_K391_OMSDLAM_U_V1.BDS
      ROS_CG_K760_OMSDLAM_U_V1.BDS
      ROS_CG_M001_OMSDLAM_U_V1.BDS  Contains 67P/C-G shape data based
                                    on OSIRIS images produced by LAM
                                    using MSPCD method with plate
                                    numbers from 6K to 1M, for use with
                                    Toolkits N0065 or earlier.

      ROS_CG_K006_OSPCLPS_U_V1.BDS
      ROS_CG_K012_OSPCLPS_U_V1.BDS
      ROS_CG_K024_OSPCLPS_U_V1.BDS
      ROS_CG_K050_OSPCLPS_U_V1.BDS
      ROS_CG_K096_OSPCLPS_U_V1.BDS
      ROS_CG_K195_OSPCLPS_U_V1.BDS
      ROS_CG_K399_OSPCLPS_U_V1.BDS
      ROS_CG_K786_OSPCLPS_U_V1.BDS  Contains 67P/C-G shape data based
                                    on OSIRIS images produced by
                                    LAM-PSI using SPC method with plate
                                    numbers from 6K to 3M, for use
                                    with Toolkits N0065 or earlier.

      ROS_CG_M004_NSPCESA_U_V1.BDS
      ROS_CG_K250_NSPCESA_U_V1.BDS
      ROS_CG_K104_NSPCESA_U_V1.BDS
      ROS_CG_M002_NSPCESA_U_V1.BDS  Contains 67P/C-G shape data based
                                    on NAVCAM images produced by ESA
                                    using SPC method with plate numbers
                                    from 104K to 4M plates, for use
                                    with Toolkits N0065 or earlier.

      ROS_CG_K050_OSPGDLR_U_V1.BDS
      ROS_CG_K100_OSPGDLR_U_V1.BDS
      ROS_CG_K200_OSPGDLR_U_V1.BDS
      ROS_CG_M001_OSPGDLR_U_V1.BDS
      ROS_CG_M004_OSPGDLR_U_V1.BDS  Contains 67P/C-G shape data based on
                                    OSIRIS images produced by DLR using
                                    the SPG method with plate numbers
                                    from 50K to 4M, for use with
                                    Toolkits N0065 or earlier.

   Asteroid 21 Lutetia DSKs, for use with Toolkit N0066 or later:

      ROS_LU_K003_OSPCLAM_N_V1.BDS
      ROS_LU_K006_OSPCLAM_N_V1.BDS
      ROS_LU_K012_OSPCLAM_N_V1.BDS
      ROS_LU_K025_OSPCLAM_N_V1.BDS
      ROS_LU_K048_OSPCLAM_N_V1.BDS
      ROS_LU_K098_OSPCLAM_N_V1.BDS
      ROS_LU_K190_OSPCLAM_N_V1.BDS
      ROS_LU_K240_OSPCLAM_N_V1.BDS
      ROS_LU_K380_OSPCLAM_N_V1.BDS
      ROS_LU_K780_OSPCLAM_N_V1.BDS
      ROS_LU_M002_OSPCLAM_N_V1.BDS
      ROS_LU_M003_OSPCLAM_N_V1.BDS  Contains Lutetia shape data based on
                                    OSIRIS images produced by LAM using
                                    SPC method with plate numbers from
                                    3K to 3M, for use with Toolkits
                                    N0066 or later.

   Asteroid 21 Lutetia DSKs, for use with Toolkit N0065 or earlier:

      ROS_LU_K003_OSPCLAM_U_V1.BDS
      ROS_LU_K006_OSPCLAM_U_V1.BDS
      ROS_LU_K012_OSPCLAM_U_V1.BDS
      ROS_LU_K025_OSPCLAM_U_V1.BDS
      ROS_LU_K048_OSPCLAM_U_V1.BDS
      ROS_LU_K098_OSPCLAM_U_V1.BDS
      ROS_LU_K190_OSPCLAM_U_V1.BDS
      ROS_LU_K240_OSPCLAM_U_V1.BDS
      ROS_LU_K380_OSPCLAM_U_V1.BDS
      ROS_LU_K780_OSPCLAM_U_V1.BDS
      ROS_LU_M002_OSPCLAM_U_V1.BDS
      ROS_LU_M003_OSPCLAM_U_V1.BDS  Contains Lutetia shape data based on
                                    OSIRIS images produced by LAM using
                                    SPC method with plate numbers from
                                    3K to 3M, for use with Toolkits
                                    N0065 or earlier.


   Asteroid 2867 Steins DSKs, for use with Toolkit N0066 or later:

      ROS_ST_K020_OSPCLAM_N_V1.BDS  Contains Steins shape data based on
                                    OSIRIS images produced by LAM using
                                    SPC method with 20K plates, for use
                                    with Toolkits N0066 or later.


   Asteroid 2867 Steins DSKs, for use with Toolkit N0065 or earlier:

      ROS_ST_K020_OSPCLAM_U_V1.BDS  Contains Steins shape data based on
                                    OSIRIS images produced by LAM using
                                    SPC method with 20K plates, for use
                                    with Toolkits N0065 or earlier.


   Solar System Bodies DSKs, for use with Toolkit N0066 or later:

      PHOBOS_K275_DLR_V02.BDS       Contains Phobos shape data based on
                                    Mars-Express HRSC images.

      PHOBOS_M003_GAS_V01.BDS       Contains Phobos shape data by Robert
                                    Gaskell based on Viking Orbiter 1 VIS-A
                                    and VIS-B camera images.

      DEIMOS_K005_THO_V01.BDS       Contains Deimos shape data by Peter
                                    Thomas based on Viking Orbiter images.

      TEMPEL1_9P_K032_THO_V01.BDS   Contains 9P/Tempel 1 comet shape data by
                                    Peter Thomas based on Deep Impact and
                                    Stardust spacecraft data.


   Rosetta spacecraft structures DSKs, for use with Toolkit N0066 or later:

      ROS_SC_BUS_Vvv.BDS               SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta spacecraft
                                       Bus, for named surface.
                                       To be used with SPICE toolkit N0066
                                       or later. Created by the ESA SPICE
                                       Service.

      ROS_SC_BUS_LR_Vvv.BD             SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta spacecraft
                                       Bus with the Rosetta lander attahced,
                                       for named surface. To be used with
                                       SPICE toolkit N0066 or later.
                                       Created by the ESA SPICE Service.

      ROS_SC_SAPY_Vvv.BDS              SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta spacecraft
                                       +Y Solar Array, for named surface.
                                       To be used with SPICE toolkit N0066
                                       or later. Created by the ESA SPICE
                                       Service.

      ROS_SC_SAMY_Vvv.BDS              SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta spacecraft
                                       -Y Solar Array, for named surface.
                                       To be used with SPICE toolkit N0066
                                       or later. Created by the ESA SPICE
                                       Service.

      ROS_SC_HGA_Vvv.BDS               SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta spacecraft
                                       High Gain Antenna, for named surface.
                                       To be used with SPICE toolkit N0066
                                       or later. Created by the ESA SPICE
                                       Service.

      ROS_LR_D_Vvv.BDS                 SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta lander with
                                       deployed structures, for named surface.
                                       To be used with SPICE toolkit N0066
                                       or later. Created by the ESA SPICE
                                       Service.

      ROS_LR_R_Vvv.BDS                 SPICE Digital Shape Kernel (DSK)
                                       file for the Rosetta lander with
                                       retracted structures, for named surface.
                                       To be used with SPICE toolkit N0066
                                       or later. Created by the ESA SPICE
                                       Service.


-------------------

        This file was last modified on July 31, 2020  (M. Costa)