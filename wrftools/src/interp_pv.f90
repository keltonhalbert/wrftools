SUBROUTINE INTERP_PV(PV_GRID, DATA_GRID, INTERPLEVELS, OUT_GRID)
!       This function takes a 3D PV grid 
!       and another field of data on the same grid
!       and interpolates it to the given interp 
!       levels.
        IMPLICIT NONE 
        REAL, DIMENSION(:,:,:,:), INTENT(IN) :: PV_GRID
        REAL, DIMENSION(:,:,:,:), INTENT(IN) :: DATA_GRID
        REAL, DIMENSION(:), INTENT(IN) :: INTERPLEVELS
        REAL, DIMENSION(21,20,375, 375), INTENT(OUT) :: OUT_GRID       
        INTEGER, DIMENSION(SIZE(SHAPE(PV_GRID)))  :: PV_SHAPE
        INTEGER, DIMENSION(SIZE(SHAPE(DATA_GRID))) :: GRID_SHAPE
        INTEGER WEST_EAST, SOUTH_NORTH, BOTTOM_TOP
        INTEGER I, J, K, LEV, TIME, T
        REAL PV_BOT, PV_TOP, PV_NBR, GRD_BOT, GRD_TOP
        LOGICAL FLAG

!       Get the shapes of the grids to make sure they are the
!       same
        GRID_SHAPE = SHAPE(DATA_GRID) 
        PV_SHAPE = SHAPE(PV_GRID)
        TIME = PV_SHAPE(1)
        BOTTOM_TOP  = PV_SHAPE(2)
        SOUTH_NORTH = PV_SHAPE(3)
        WEST_EAST = PV_SHAPE(4)
        
!       Check to make sure the grids are the same shape. If they
!       are not, print the error message and exit the function.
!       Otherwise, continue working.
        IF ( (TIME == GRID_SHAPE(1)) .AND. (BOTTOM_TOP == GRID_SHAPE(2)) .AND. &
        (SOUTH_NORTH == GRID_SHAPE(3)) .AND. (WEST_EAST == GRID_SHAPE(4)) ) THEN
            CONTINUE 
        ELSE
            PRINT*, "ARRAY SIZE MISMATCH", PV_SHAPE, GRID_SHAPE
            RETURN
        END IF

!        ALLOCATE(OUT_GRID(TIME, SIZE(INTERPLEVELS), SOUTH_NORTH, WEST_EAST)) 
!       Loop over the contents of the arrays
        DO T = 1, TIME
            DO I = 1, WEST_EAST
                DO J = 1, SOUTH_NORTH
                    FLAG = .FALSE.
                    DO LEV = 1, SIZE(INTERPLEVELS)
                        DO K = BOTTOM_TOP-1, 1, -1
                            PV_BOT = PV_GRID(T, K, J, I)
                            GRD_BOT = DATA_GRID(T, K, J, I)

                            PV_TOP = PV_GRID(T, K+1, J, I)
                            GRD_TOP = DATA_GRID(T, K+1, J, I)
                            
                            PV_NBR = PV_GRID(T, MAX(K-2, 1), J, I) 

                            IF ( (PV_BOT >= INTERPLEVELS(LEV)) .AND. (K == 1)) THEN
                                OUT_GRID(T, LEV, J, I) = GRD_BOT

                            ELSE IF ( (PV_TOP >= INTERPLEVELS(LEV)) .AND. (PV_BOT <= INTERPLEVELS(LEV)) &
                            .AND. (PV_NBR <= INTERPLEVELS(LEV))) THEN 
                                OUT_GRID(T, LEV, J, I) = GRD_BOT + (GRD_TOP - GRD_BOT) * &
                                ((INTERPLEVELS(LEV) - PV_BOT)/(PV_TOP - PV_BOT))
                                EXIT
                            ELSE IF ((PV_GRID(T, BOTTOM_TOP, J, I) < INTERPLEVELS(LEV)) .AND. (K==1)) THEN
                                OUT_GRID(T, LEV, J, I) = DATA_GRID(T, BOTTOM_TOP, J, I)
                            END IF 
                        END DO
                    END DO
                END DO
            END DO 
        END DO

END SUBROUTINE INTERP_PV
