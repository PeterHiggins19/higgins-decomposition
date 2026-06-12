# Higgins Diagrams
## A Diagrammatic Language for Compositional Data Dissection
### Peter Higgins — April 2026

---

## Prior Art Search

| Term searched                        | Result     |
|--------------------------------------|------------|
| "Higgins Diagrams"                   | No match   |
| "Higgins Diagram" + mathematics      | No match   |
| "Higgins Diagram" + statistics       | No match   |
| "Higgins Diagram" + category theory  | No match   |
| "Higgins Diagram" + data viz         | No match   |
| "Higgins Decomposition Diagram"      | No match   |

Philip Higgins (1926-2015) published on categories and groupoids.
No diagram type bears the name. The term is unoccupied.

**Claim: "Higgins Diagrams" — diagrammatic language for compositional
data analysis on the Aitchison simplex, originated by Peter Higgins, 2026.**

---

## Design Principles

    1. 7-bit ASCII only (0x20-0x7E)
    2. No colour dependency — readable on monochrome output
    3. No font dependency — fixed-width rendering assumed
    4. Every symbol has exactly one meaning
    5. Composable — diagrams nest and chain
    6. Wordless — the notation carries the semantics
    7. Scale-free — same symbols at any resolution

---

## The Alphabet

### Part Symbols (Components of the Composition)

    x    single part (generic component)
    x_i  indexed part (i = 1..D)
    [x]  closed part (after simplex closure)
    {x}  grouped part (after amalgamation)

### Composition Symbols

    ( x1 x2 ... xD )     open composition (raw)
    [ x1 x2 ... xD ]     closed composition (simplex)
    < x1 x2 ... xD >     transformed composition (CLR/ILR)

### Boundary Markers

    |    simplex boundary (sum constraint)
    ||   hard boundary (zero component — structural absence)
    :    partition boundary (amalgamation group edge)

### Operators

    /    ratio (x_i / x_j)
    //   log-ratio (ln(x_i / x_j))
    /_\  geometric mean (denominator of CLR)
    S    closure operator (divide by sum)
    C    CLR transform operator
    V    variance accumulator
    T    shape classifier (HVLD)
    L    lock detector
    P    pair ranker
    A    amalgamation operator
    E    decimation operator (EITT)

### Flow Arrows

    ->   forward transform (input to output)
    =>   projection (dimension reduction)
    ~>   approximation (fitted curve)
    |>   classification output (diagnosis)
    >>   compression (decimation)

### Shape Glyphs

    /\    DOME (concave-down parabola — convergent system)
    \/    BOWL (concave-up parabola — divergent system)
    --    GEODESIC (flat trajectory — stable system)
    /\/\  CHAOTIC (no fit — disordered system)

### Lock Glyphs

    @    lock point (trajectory touches constant)
    @c   lock to specific constant c
    @pi  lock to pi
    @e   lock to e
    @ln2 lock to ln(2)
    @phi lock to phi (golden ratio)
    @sr2 lock to sqrt(2)

    (d)  delta — distance to lock
    [@c (d)] lock declaration: constant c, distance d

### Stability Glyphs

    =    stable pair (low CV, components coupled)
    ~    drifting pair (medium CV)
    #    volatile pair (high CV, substitution underway)
    x_i = x_j     pair i,j is locked
    x_i # x_j     pair i,j is substituting
    x_i ~ x_j     pair i,j is drifting

### Trajectory Marks

    .    single time point on trajectory
    ..   trajectory segment
    ...  full trajectory (all time points)
    .@.  trajectory passing through lock point
    .^.  trajectory at apex (dome peak)
    .v.  trajectory at nadir (bowl bottom)

### Dimensional Markers

    S^n   n-simplex (D parts on (D-1)-simplex)
    S^8   8-simplex (9 parts)
    S^7   7-simplex (8 parts)
    S^2   2-simplex (3 parts, ternary)

    S^8 => S^2   amalgamation from 9 parts to 3

### Decimation Markers

    >>2   2x temporal compression
    >>4   4x temporal compression
    >>8   8x temporal compression

    V...  = V>>2...  entropy invariance holds
    V... != V>>2...  entropy invariance fails

---

## The Eight Projection Diagrams

Each Hs stage produces exactly one Higgins Diagram type.
The diagram type is named by its operator letter.

### HD-S : The Closure Diagram

Shows raw parts becoming proportions. Total removed.

    ( 148 49 25 170 )  ->  S  ->  [ .38 .13 .06 .43 ]
      raw counts              |       proportions
                              |
                          392 discarded

    Notation:

    ( x1 x2 x3 x4 )
    ----+---+---+----
        |   |   |
        S   S   S        closure applied to each
        |   |   |
    ----+---+---+----
    [ .  .  .  .  ]      sum = 1

    Projection: absolute -> relative
    Discards:   total magnitude
    Reveals:    share structure

### HD-C : The Centre Diagram

Shows each part measured against the geometric mean.

    [ x1  x2  x3 ]            closed composition
         |
        /_\                    geometric mean computed
         |
    < ln(x1/g)  ln(x2/g)  ln(x3/g) >    CLR coordinates

    Notation:

         /_\  = g(x)
          |
    x_i --//-- g  ->  c_i     each part log-ratioed to centre

    Key property:  sum(c_i) = 0  always

    Projection: curved simplex -> flat Euclidean
    Discards:   curvature constraint
    Reveals:    displacement from geometric centre

### HD-V : The Trajectory Diagram

Cumulative variance across time. The heartbeat.

    t=0  t=1  t=2  t=3  t=4  t=5  ...  t=T
     .    .    .    .    .    .         .
     0   3.2  3.1  2.7  2.4  2.2      6.4
     |    |    |    |    |    |         |
     +----+----+----+----+----+-- V -->+
               the trajectory

    Notation:

    V(t) = sum_i Var(CLR_i, 1..t)

    V: . . . . . . . . . . . . . . .
       |                           |
       0                          V_T

    Projection: D-dimensional CLR -> scalar curve
    Discards:   individual carrier identity
    Reveals:    total system dispersion over time

### HD-T : The Shape Diagram

Parabola fitted to trajectory. System classified.

    V(t):  . . . . .^. . . . .       observed
           ~  ~  ~  ~  ~  ~  ~       fitted parabola
                    ^
                  apex

    Shape classification:

    /\   a < 0   DOME    (system converging)
    \/   a > 0   BOWL    (system diverging)
    --   a ~ 0   GEODESIC (system stable)
    /\/\ R2 < t  CHAOTIC  (no coherent shape)

    Notation:

    HD-T:  V... ~> (a,b,c)  |>  /\
                   fit         shape

    Example (Germany):
    V... ~> (-0.00013, 0.130, 1.854)  |>  /\  R2=0.665

    Projection: trajectory curve -> single shape class
    Discards:   trajectory detail
    Reveals:    system regime (expanding/contracting/stable)

### HD-L : The Lock Diagram

Where trajectory passes near transcendental constants.

    V(t):  . . . .@. . . . . .
                  |
                  | (d) = 0.002
                  |
           ------pi------        constant line

    Notation:

    .@.  [@pi (0.002)]    lock at t, constant pi, delta 0.002

    Multiple locks:

    . . .@e. . .@pi. . . . .
          |      |
          e     pi
       (0.003) (0.002)

    Lock declaration:

    HD-L:  V(9) = 3.149  [@pi (0.002)]
           V(8) = 2.710  [@e  (0.003)]

    Projection: trajectory values -> structural addresses
    Discards:   trajectory shape
    Reveals:    proximity to fundamental geometric ratios

### HD-P : The Pair Diagram

All D(D-1)/2 log-ratio pairs ranked by stability.

    x_i // x_j    CV%     class
    -----------    ----    -----
    Coal // OFos   13.0    =       stable (coupled)
    Coal // Hydr   14.0    =       stable
    Gas  // OFos   14.8    =       stable
    Gas  // Hydr   16.6    =       stable
    Coal // Gas    39.5    ~       drifting
    ...
    Nucl // Solr  485.6    #       volatile (substituting)
    Nucl // Wind  664.4    #       volatile

    Notation:

    =  CV <  25%     locked pair
    ~  CV 25-100%    drifting pair
    #  CV > 100%     substituting pair

    Compact form:

    HD-P:  Coal = OFos = Hydr = Gas
           Coal ~ Gas
           Nucl # Solr # Wind

    Reading: Coal, Other Fossil, Hydro, Gas form a
    stable cluster. Nuclear is substituting with
    Solar and Wind.

    Projection: D(D-1)/2 ratios -> ranked stability list
    Discards:   absolute CLR values
    Reveals:    which parts move together, which replace each other

### HD-A : The Amalgamation Diagram

Carriers merged into coarser groups. Classification tested.

    S^8                              S^2
    [ Bio Coal Gas Hyd Nuc OFs ORn Sol Win ]
      |   |    |   |   |   |   |   |   |
      :---+----+---:   :   :---+---+---:
      |  Fossil    | Nuclear | Renewable |
      :            :         :           :
    [ .F           .N         .R         ]

    Notation:

    HD-A:  S^8 => S^2
           {Coal Gas OFos} : {Nucl} : {Bio Hyd ORn Sol Win}
           /\ (S^8) = /\ (S^2)     classification preserved
                                    AMALGAMATION STABLE

    If classification changes:

           /\ (S^8) != -- (S^2)    classification NOT preserved
                                   AMALGAMATION SENSITIVE

    Projection: D-part simplex -> K-part simplex (K < D)
    Discards:   within-group structure
    Reveals:    whether diagnosis is resolution-dependent

### HD-E : The Decimation Diagram

Temporal compression. Entropy invariance tested.

    V:  . . . . . . . . . . . . . . . .    1x (26 points)
    V>>2:  .   .   .   .   .   .   .   .    2x (13 points)
    V>>4:  .       .       .       .        4x (7 points)
    V>>8:  .               .               8x (4 points)

    Notation:

    HD-E:  H(V) = 4.231
           H(V>>2) = 4.198
           H(V>>4) = 4.185

           H(V) = H(V>>2) = H(V>>4)    EITT HOLDS
                                        shape is intrinsic

    Or:

           H(V) != H(V>>2)             EITT FAILS
                                        shape is sampling artefact

    Projection: trajectory at resolution k -> scalar entropy
    Discards:   temporal detail
    Reveals:    whether structure is scale-independent

---

## Composition Rules

Higgins Diagrams compose left to right. The full pipeline:

    HD-S -> HD-C -> HD-V -> HD-T -> HD-L
                      |
                      +-> HD-P
                      |
                      +-> HD-A -> HD-T (verify)
                      |
                      +-> HD-E

### Pipeline Notation (Compact)

    ( x ) -> S -> C -> V -> T |> /\  R2=0.665
                         V -> L [@pi (0.002)]
                         V -> P [Coal=OFos, Nucl#Sol]
                    C -> A -> T |> /\  (preserved)
                         V -> E [H=H>>2 INVARIANT]

### Full System Declaration

    Hs( Germany, 2000-2025, S^8 )
    ================================
    HD-S: (9 carriers) -> [9 proportions]
    HD-C: [9] -> <9 CLR>  sum=0
    HD-V: <9 CLR, 26yr> -> V(t)  0..6.43
    HD-T: V ~> /\  R2=0.665  DOME
    HD-L: V(9)=3.149  [@pi (0.002)]
           V(8)=2.710  [@e  (0.003)]
    HD-P: Coal=OFos (13%) Coal=Hydr (14%)
           Nucl#Sol (486%) Nucl#Wind (664%)
    HD-A: S^8 => S^2  /\ = /\  STABLE
    HD-E: H=H>>2  INVARIANT
    ================================

---

## Comparative Notation

Multiple systems side by side:

    System     HD-T   HD-L           HD-P (top)     HD-A
    --------   ----   -----------    -----------     ----
    Germany    /\     @pi (0.002)    Coal=OFos 13%  /\=/\
    Japan      /\     @ln10(0.000)   Bio=Coal  10%  /\=/\
    UK         /\     @lnpi(0.006)   Gas=OFos   8%  /\=/\
    France     /\     @sr2 (0.007)   Nuc=ORn    3%  /\=/\

Reading: All four systems are DOME. Each locks to a
different constant. France is the most stable (CV=3%).
All are amalgamation-stable.

---

## Tomosynthesis

The Higgins Diagram set is a tomosynthesis of compositional data.
Each diagram type is a projection from a different angle through
the same compositional object. No single diagram is the diagnosis.
The set is the instrument.

    Angle        Diagram   Sees                 Blind to
    ---------    -------   ----                 --------
    Magnitude    HD-S      relative shares      total size
    Geometry     HD-C      centre displacement   curvature
    Time         HD-V      dispersion history    carrier ID
    Shape        HD-T      regime class          detail
    Address      HD-L      constant proximity    dynamics
    Coupling     HD-P      pair relationships    trajectory
    Resolution   HD-A      scale independence    within-group
    Frequency    HD-E      temporal invariance   spatial

    Together: complete structural reconstruction.

---

## Symbol Summary Table

    Symbol   Meaning                  Context
    ------   -------                  -------
    x        part                     generic
    x_i      indexed part             specific
    [x]      closed part              post-closure
    {x}      grouped part             post-amalgamation
    ( )      open composition         raw data
    [ ]      closed composition       simplex
    < >      transformed composition  CLR/ILR
    |        simplex boundary         constraint
    ||       hard boundary            structural zero
    :        partition boundary       amalgamation edge
    /        ratio                    x_i/x_j
    //       log-ratio                ln(x_i/x_j)
    /_\      geometric mean           CLR denominator
    ->       forward transform        input to output
    =>       projection               dimension reduction
    ~>       approximation            curve fit
    |>       classification           diagnosis output
    >>       compression              decimation
    /\       DOME                     a < 0
    \/       BOWL                     a > 0
    --       GEODESIC                 a ~ 0
    /\/\     CHAOTIC                  low R2
    @        lock point               trajectory near constant
    (d)      delta                    lock distance
    =        stable pair              CV < 25%
    ~        drifting pair            CV 25-100%
    #        volatile pair            CV > 100%
    .        time point               single observation
    ..       trajectory segment       partial path
    ...      full trajectory          all observations
    .@.      lock passage             trajectory at constant
    .^.      apex                     dome peak
    .v.      nadir                    bowl bottom
    S^n      n-simplex                dimension marker
    >>k      k-fold decimation        temporal compression
    H( )     Shannon entropy          invariance test
    Hs( )    full pipeline call       system declaration

---

## Reading a Higgins Diagram

No words needed. The notation is self-documenting.

    Hs( X, S^8 )  |>  /\  @pi  Coal=Gas  Nucl#Sol  /\=/\  H=H>>2

Reads: System X on the 8-simplex is classified DOME,
locks to pi, Coal and Gas are coupled, Nuclear is
replacing Solar, the classification survives amalgamation,
and the trajectory shape is scale-invariant.

One line. Any language. Any reader.

---

*Peter Higgins*
*Rogue Wave Audio — Markham, Ontario*
*April 2026*
