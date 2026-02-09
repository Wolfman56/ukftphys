5
2
0
2

b
e
F
8

]
c
q
-
r
g
[

7
v
1
9
3
4
1
.
8
0
4
2
:
v
i
X
r
a

Gravity from entropy

Ginestra Bianconi1, ∗
1School of Mathematical Sciences, Queen Mary University of London, London, E1 4NS, United Kingdom

Gravity is derived from an entropic action coupling matter fields with geometry. The fundamental
idea is to relate the metric of Lorentzian spacetime to a quantum operator, playing the role of an
renormalizable effective density matrix and to describe the matter fields topologically, according to
a Dirac-K¨ahler formalism, as the direct sum of a zero-form, a one-form and a two-form. While the
geometry of spacetime is defined by its metric, the matter fields can be used to define an alternative
metric, the metric induced by the matter fields, which geometrically describes the interplay between
spacetime and matter. The proposed entropic action is the quantum relative entropy between the
metric of spacetime and the metric induced by the matter fields. The modified Einstein equations
obtained from this action reduce to the Einstein equations with zero cosmological constant in the
regime of low coupling. By introducing the G-field, which acts as a set of Lagrangian multipliers, the
proposed entropic action reduces to a dressed Einstein-Hilbert action with an emergent small and
positive cosmological constant only dependent on the G-field. The obtained equations of modified
gravity remain second order in the metric and in the G-field. A canonical quantization of this field
theory could bring new insights into quantum gravity while further research might clarify the role
that the G-field could have for dark matter.

I.

INTRODUCTION

The relation between general relativity, statistical me-
chanics and information theory is a central research topic
in theoretical physics. The interest in the subject has its
roots in the discovery that black holes have an entropy
[1, 2] and emit Hawking radiation [3]. Recently, impor-
tant results have been obtained relating information the-
ory, entanglement entropy [4–6] and gravity [7–13] involv-
ing the holographic principle [14–16], the entanglement
properties of quantum field theory and the theory of von
Neumann algebras [17, 18].

These results define a very active research direction
[19] indicating that the quest for an ultimate gravita-
tional theory based on information theory and statistical
mechanics is ongoing. A comprehensive statistical me-
chanics approach to gravity is expected to give rise to
modified Einstein equations [20–22] that on the one side
can be testable experimentally [23, 24] while on the other
side can bring important conceptual insights into the ul-
timate theory for black holes [25], dark matter [26] and
quantum gravity [27–32].

In this work, a continuum modified theory of grav-
ity based on a statistical mechanics action is considered.
This theory treats the metric at each point of spacetime
as a “renomalizable” density matrix, or more precisely a
local quantum operator. This central idea is relating
geometry with the mathematical foundation of quantum
field theory [33] and is inspired by the used of von Neu-
mann algebras in explaining entanglement in field theo-
ries [17, 18] and quantum gravity [34–36]. While the
geometry of spacetime is defined through its associated
metric, the interplay between matter fields and geometry
is captured by the metric induced by the matter fields

∗ ginestra.bianconi@gmail.com

which describes how the matter fields effectively curve
spacetime. Embracing a statistical mechanics approach
to gravity, this work interprets these metric tensors as
quantum operators and postulates an action for gravity
given by the quantum relative entropy between the met-
ric of the manifold and the metric induced by the matter
fields. From the mathematical point of view, the quan-
tum relative entropy proposed in this work is strictly
related to the Araki quantum relative entropy for von
Neumann algebras [17, 37–39]. From the physics point
of view, the proposed action fully describes how matter
curves geometry and how geometry affects the matter
fields.

A crucial aspect of the proposed theory is the adoption
of a topological (Dirac-K¨ahler like [40, 41]) description of
bosonic matter fields. Note that the extension of Dirac-
K¨ahler and staggered fermions formalism to bosonic par-
ticles is gaining increasing interest in lattice gauge the-
ory [42, 43] and in network theory as well [44]. These
bosonic matter fields are described as the direct sum of
a 0-form, a 1-form, and a 2-form defined on the Rieman-
nian manifold describing spacetime. Moreover the met-
ric induced by the topological matter fields is expressed
in terms of the Hodge-Dirac operator [45]. From this
statistical mechanics approach to gravity we derive the
modified Einstein equations by introducing an auxiliary
field associated to gravity which we call G-field. The in-
troduction of this new field is justified as it acts as a
set of Lagragian multipliers enforcing linear constraints
on metric induced by the matter fields. In this way the
G-field extends the popular use of the Legendre trans-
formation in f (R) theories [20, 22]. Given the particular
entropic structure of the action, the modified Einstein
equations take a very simplified expression. The grav-
itational part of the action takes the form of a dressed
Einstein-Hilbert action in which we observe an emergent
positive cosmological constant that depends exclusively
on the G-field.

This work greatly expands on previous results [44] ob-
tained in the discrete setting by the same author. On
one side, here a continuum and fully Lorentz invariant
theory is proposed. This progress is based on the devel-
opment of the suitable mathematical framework to define
the Lorentz invariant entropy and cross-entropy between
the metric of the spacetime and the metric induced by
the matter fields. On the other side, here the relation of
this statistical mechanics/information theory action with
the Einstein-Hilbert action [46, 47] is established defining
a clear connection to gravity. Two fundamental aspects
of this work that are not present in Ref. [44], are relevant
to clearly relate this approach to gravity. First, this work
considers a local theory, defining the entropy of the met-
ric at each point of spacetime, while the previous work
considers only the entropy associated to the full metric of
the higher-order network. The present local theory allows
a closer connection to gravity and constitutes a step for-
ward to establish the connection between this approach
and the quantum theory of entanglement [17]. Secondly,
by adopting the continuum limit, in this work the intrin-
sic difficulty related to the definition of the curvature of
networks, simplicial and cell complexes is avoided.

To keep the discussion concise the focus is here
mostly on scalar (bosonic) matter fields, and their
topological generalizations with a brief mention in
Appendix A to the natural extension of this framework
to Abelian gauge fields, while in Ref. [44] the theory
Further exten-
covers also fermionic matter fields.
sions of the proposed local framework to Dirac and
non-Abelian gauge fields [44, 48, 49] in the continuum
or in the discrete setting are left for future investigations.

This work is structured as follows. In Sec. II we pro-
vide the motivation of the proposed theory and we discuss
preliminary results on an instructive warm-up scenario.
In Sec.
III we outline the proposed theoretical frame-
work, we postulate the entropic action for gravity and we
derive the corresponding modified Einstein equations. In
Sec.IV we provide the concluding remarks. The paper
also includes three Appendices discussing possible exten-
sions of the proposed theoretical framework, providing
the mathematical background and all the necessary de-
tails regarding the notation used Sec. III, and establish-
ing the connection of the present theory with the theory
of local quantum operators and the Araki entropy.

II. MOTIVATION OF THE THEORY AND
PRELIMINARY CONSIDERATIONS

A. Eigenvalues and logarithm of rank 2-tensors

2

tical mechanics and information theory action for gravity,
we need first to define the eigenvalues the logarithm of
rank-2 tensors ˆG. To this end we first define the eigen-
values λ and eigenvectors V (λ)
of the covariant tensor ˆG
ν
of elements ˆGµν in a Lorentz invariant way. These satisfy
the eigenvalue problem

ˆGµν[V (λ)]ν = λV (λ)
µ .

(1)

We say that a rank-2 tensor is positively defined if all its
eigenvalues are positive. We notice that this definition of
the eigenvalue of a rank-2 tensor reduces to the definition
of the eigenvalue of the matrix ˆGg−1 as Eq.(1) can be
rewritten as

ˆGµσgσν[V (λ)]ν = λV (λ)
µ .

(2)

One striking consequence of this definition is that the
eigenvalues of the metric gµν are all identically equal to
one.

Assuming that the tensor ˆGµν is positively defined, we

define the logarithm of this tensor as

[ln( ˆG)]µν = V (λ)

µ V (λ)
ν

ln(λ).

and the inverse of a tensor as

[ ˆG−1]µν = [V (λ)]µ[V (λ)]νλ−1.

(3)

(4)

It follows that if the tensor ˆG is invertible, the logarithm
of the inverse of a positively defined tensor is given by

[ln( ˆG−1)]µν = −[V (λ)]µ[V (λ)]ν ln(λ).

(5)

Finally we define the trace of a rank two tensor as the
sum of its eigenvalues, i.e.

Tr ˆG =

(cid:88)

λ.

λ

(6)

Thus the trace of a rank-2 tensor can be also calculated
as usual in tensor calculus, as the trace of the matrix
ˆGg−1, i.e.

Tr ˆG = TrM ˆGg−1 = ˆGµνgµν.

(7)

In this first section we are interested exclusively on rank-
two tensors that are metrics between vectors (and 1-
forms). In the subsequent paragraphs and in Appendix B
we will extended the notion of eigenvalues also to metric
matrices between bivectors (and 2-forms) represented by
rank-4 tensors. Such an approach will be shown in Ap-
pendix B to be general and applicable to metric tensors
between two n-vectors (an n-forms) with n of any order.

Spacetime is described by a torsion free, d-dimensional
Riemannian manifold K associated with a Lorentzian
metric gµν of signature {−1, 1, , 1 . . . , 1} and a metric
compatible Levi-Civita connection Γσ
νµ determining the
covariant derivative ∇µ. In order to formulate our statis-

Before we develop our theory, let us consider an in-
structive warm-up scenario that will help justify the the-
ory that we will present in the following. Having de-
fined the logarithm of positively defined rank-2 tensors,

B. Warm-up scenario: Entropic action

3

Covariant Metrics Elements

g
G
ˆG

gµν
Gµν
ˆGµν

Definition
Default covariant rank-2 metric tensor between vectors associated to the manifold K
Covariant rank-2 metric between vectors induced by the matter fields
General covariant rank-2 metric tensor including both g and G

TABLE I. Notation used to indicate the different metrics in the warm-up-scenario

we are now in the position to define their Lorentz invari-
ant quantum entropy H for metric associated to 1-forms.
This is inspired by the expression of the Von Neumann
entropy albeit we do not require the tensor to have trace
one at every point in spacetime. Thus strictly speak-
ing we interpret the generic metric tensor as a quantum
operator [33], which has the physical interpretation of
a renormalizable effective density matrix [18]. We con-
sider positive definite, invertible metric for 1-forms, rep-
resented by the covariant tensor ˆG of rank two. We define
the entropy H of ˆG as

H = Tr ˆG ln ˆG−1 = ˆGµν[ln ˆG−1]νµ = −

(cid:88)

λ ln λ.

(8)

Note that the problem of defining eigenvalues and en-
tropy of tensors is a topic of intense research and similar
definitions have been provided for instance in the theory
of elasticity [50] and in applied tensor analysis [51] (al-
though not defined in a Lorentz invariant way). In the
present warm-up scenario we will define the entropy and
the quantum relation entropy of different metrics taking
the form of rank-2 tensors. As a reference for the no-
tation used, the reader can refer to Table I. Recalling
that the metric g has all the eigenvalues equal to one, it
follows that the entropy of the metric g is null, i.e.

H = Trg ln g−1 = 0.

(9)

The fundamental assumption of the present theory is
that spacetime is endowed with two metrics: the met-
ric g fully determining the spacetime geometry and the
metric induced by the matter fields G that fully capture
the interplay between matter fields and geometry. Leav-
ing the detailed discussion about the metric induced by
the matter fields to the next paragraph, we postulate
that the action should explicitly express the relation be-
tween these two metrics and their reciprocal coupling. By
embracing a statistical mechanics approach we consider
the Lagrangian L given by the quantum relative entropy
between the metric g and the metric G induced by the
matter field defined as

L = −Trg ln g−1 + Trg ln G−1.

(10)

Using H = 0 we thus obtain:

L = Trg ln G−1.

(11)

We observe that since g has all the eigenvalues equal to
the identity, and Eq.(2) holds for ˆG = G, the Lagrangian
L can be also be expressed as

L ≡ −TrM ln Gg−1 = −

ln(λ′),

(12)

(cid:88)

λ′

where with TrM ln Gg−1 we indicate the usual trace of
the logarithm of the matrix ln Gg−1 and with λ′ the
eigenvalues of the 2-tensor G as defined in Eq.(2).

An important point here is that the Lorentz invari-
ant definition of the quantum relative entropy given by
Eq.(12) requires that the matrix G has to be invertible as
well as the matrix g. Thus this is another difference with
respect to the strictly speaking density matrices that can
be semi-definite positive. We are now in the position to
consider an action S associated to the Lagrangian L, as
given by

(cid:90) (cid:112)| − g|Ldr,

S =

1
ℓd
P

(13)

where | − g| indicates the absolute value of the determi-
nant of g and ℓP indicates the Planck length.

We note that the quantum relative entropy [17, 37,
38] is a central quantity in quantum information [39],
in the theory of local quantum operators [33] and the
mathematical foundations of quantum gravity [34–36].
Although we are not aware of previous interpretations
of the metrics as quantum operators, it is well known that
the quantum relative entropy can also be defined among
quantum operators that generalize density matrices.
In
particular, in the fundamental theory of quantum opera-
tors algebras [37, 38], quantum operators generalize the
notion of density matrices in an analogous way of the
metric tensors adopted here. In particular in this theory,
quantum operators, like our metric matrices, might ad-
mit a finite trace at each point of the manifold but this
trace might be not unitary and might be a function of
the considered point of the manifold. For these quantum
operators the Araki quantum relative entropy [37, 38] is
defined. This entropy reduces to the von Neumann en-
tropy when the quantum operators reduces to a density
matrices of unitary trace but is defined also among quan-
tum operators of non unitary trace.

While we leave the discussion of the relation of our en-
tropic action to the Araki quantum relative entropy to
Appendix C, a series of physical observations are here in
place to justify our interpretation of the metrics matrices
as quantum operators. As remarked previously we treat
the metric tensors as quantum operators or effective den-
sity matrices. The main differences between the metric
tensor and the density operators include the fact that we
require that the metric matrices are invertible and we do
not require that they have unitary trace at each point
of the manifold. The requirement of treating exclusively

invertible metrics g and G is dictated by our desire to
define the entropy in a Lorentz invariant way.
In fact
here we desire to treat the metrics g and G on the same
footing of their inverse g−1 and G−1. It might be argued
that also our relaxation of the requirement to have den-
sity matrices of trace one, has similar roots. In fact if we
require g and G to have unitary trace at each point of
the manifold their inverse as well as their dual (defined
in Appendix C) in general will not have a unitary trace.

C. Warm-up scenario: scalar matter fields

We now apply this warm-up scenario in presence of
scalar matter fields. We consider the complex valued
scalar matter field ϕ(x) ∈ C with x ∈ K and we consider
the d-dimensional manifold immersed in K ⊗ C defined
by the points (x, ϕ(x)). The metric G induced on K by
this matter fields is given by

G = g + αM,

(14)

where α is a real positive parameter, M is the rank-2
tensor of elements

Mµν = (∇µ ¯ϕ)(∇νϕ),

(15)

where here and in the following¯˙ indicates complex conju-
gation. Since G should be adimensional it is convenient
to work in the units ℏ = c = 1 and to put α = α′ℓd
P
where ℓP is the Planck length and α′ is adimensional.

We observe that in the limit in which the field ϕ is
real, i.e. ϕ(x) ∈ R and the metric flat and Euclidean,
i.e. gµν = δµν, the metric induced by the matter fields G
given by Eq.(14) reduces to the first fundamental form of
Gauss for the d manifold immersed in Rd+1 defined by the
set of points (x, ϕ(x)). For the underlying mathematical
treatment of the metric induced by real scalar fields we
refer the interested reader to Ref. [52].

Let us define the scalar product |∇ϕ|2 as

|∇ϕ|2 = ∇µ

¯ϕgµν∇νϕ.

(16)

We observe that the inverse G−1 of the induced metric

G has metric given by

[G−1]µν = gµν − α

M µν
1 + α|∇ϕ|2 .

(17)

Adopting this notation we observe that the logarithm of
the induced metric ln G and the logarithm of ln G−1 have
elements

4

where f (w) → α for |αw| ≪ 1. With this choice of the
metric induced by the matter field we obtain that the
Lagrangian (11) reads

L = − ln(1 + α|∇ϕ|2).

(20)

We observe that in the limit α|∇ϕ| → 0 then we have
L → −α|∇ϕ|2, i.e. we recover the Lagrangian corre-
sponding to the massless Klein-Gordon equation.

By minimizing the action S with respect to the field ϕ
and to the metric g we obtain the Euler-Lagrange equa-
tions of motion:

∇µh(|∇ϕ|2)gµν∇νϕ = 0,

(21)

where h(w) is given by

h(w) =

α
1 + αw

.

(22)

In the limit αw → 0 we have h(w) → α and the equation
for the scalar field reduces to the simple massless Klein-
Gordon equation. By putting equal to zero the variation
of the action δS = 0 with respect to the metric g, we get

δS = −h(|∇ϕ|2)M µν −

1
2

Lgµν = 0.

(23)

In empty spacetime M = 0 and L = 0, thus this equation
is automatically satisfied independently on the value of
g. Thus in this limit, the metric g is not determined by
the action.
Let us now make some remarks about this warm-up
derivation. We proposed a statistical mechanics frame-
work that is very inspiring as we get the massless Klein-
Gordon equation as the outcome of the minimization of
a quantum entropy action for low coupling, i.e. 0 <
α|∇ϕ|2 ≪ 1. However this approach has two impor-
tant limitations. The first limitation is that the Klein-
Gordon equation does not contain the mass term. The
second limitation is that in absence of matter fields the
metric is not determined. In the following we provide a
more comprehensive framework to address these two lim-
itations. This framework can be related to gravity as it
gives rise to modified Einstein equations that reduce to
the Einstein equations for low coupling.

III. THE ENTROPIC THEORY OF MATTER
FIELDS COUPLED TO GEOMETRY

A. Topological matter fields and their associated
metrics

[ln G]µν = f (|∇ϕ|2)Mµν,

(cid:2)ln G−1(cid:3)µν

= −f (|∇ϕ|2)M µν,

where

f (w) =

ln(1 + αw)
w

.

(18)

(19)

In order to derive gravity from our entropic action we
need to consider the topological bosonic matter field. The
topological bosonic matter field is a type of Dirac-K¨ahler
[40, 41] boson given by the direct sum of a 0-form, a 1-
form and a 2-form. Topological bosonic fields are receiv-
ing increasing attention in discrete theories developed in

Covariant Topological Metrics
˜g = 1 ⊕ gµν dxν ⊗ dxν ⊕ [g(2)]µνρσ(dxµ ∧ dxν ) ⊗ (dxρ ∧ dxσ)

Interpretation
Default covariant topological metric between

the topological fields associated to the manifold K

˜G = G(0) ⊕ [G(1)]µν dxµ ⊗ dxν ⊕ [G(2)]µνρσ(dxµ ∧ dxν ) ⊗ (dxρ ∧ dxσ) Covariant topological metric induced by the matter fields

TABLE II. Covariant topological metrics used in the general scenario.

5

Covariant metric tensors Elements

1
gµν
[g(2)]µνρσ
G(0)

1
g
g(2)
G(0)
G(1)
G(2)

Intepretation
Default metric tensor between scalars
Default metric tensor between vectors
Default metric tensor between bivectors

Metric tensor between scalars induced by the matter fields
[G(1)]µν Metric tensor between vectors induced by the matter fields
[G(2)]µνρσ Metric tensor between bivectors induced by the matter fields

TABLE III. Covariant metric tensors between n-vectors that are included in the covariant topological metrics.

network [44] and lattice gauge theories [42, 43]. Taking
into consideration topological bosonic fields will allow us
to introduce in the metric induced by the matter fields,
terms depending on the mass of the bosonic field. Thus,
in this way, we address the first limitation of the warm-up
scenario that we have presented above.

In order to address the second limitation of the warm-
up scenario discussed previously, we include in the ex-
pression of the metric induced by the matter field, also
terms depending directly on the curvature of the mani-
fold. These terms will be expressed in terms of the Ricci
scalar R, the Ricci (covariant) tensor R of elements Rµν
and the Riemann tensor of elements Rµνρσ.

We define the topological fields |Φ⟩ as the direct sum
between a zero (complex valued) form ϕ and a (complex
valued) one-form ωµdxµ, and a (complex valued) two-
form ζµνdxµ ∧ dxν, with ζµν = −ζνµ i.e.

|Φ⟩ = ϕ ⊕ ωµdxµ ⊕ ζµνdxµ ∧ dxν,

(24)

and its conjugate topological field ⟨Φ| as

⟨Φ| = ¯ϕ ⊕ ¯ωµdxµ ⊕ ¯ζµνdxµ ∧ dxν.

(25)

The considered covariant metric ˜g is defined as the direct
sum of the metric among scalars (the identity), the metric
g among vectors introduced previously, and the metric
g(2) among bivectors given by

g(2) = gµρgνσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ),

(26)

or, exploiting the anti-symmetry of the 2-forms,

g(2) = [g(2)]µνρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ),

(27)

with

It then follows that ˜g is given by

˜g = 1 ⊕ gµνdxν ⊗ dxν

(29)

⊕[g(2)]µνρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ).

The local scalar product among topological fields is de-
fined as

⟨Φ|Φ⟩ = |ϕ|2 + ¯ωµωµ + ¯ζ µνζµν,

(30)

where ωµωµ = ωνgνµωµ, while the local outer product is
given by

|Φ⟩ ⟨Φ| = ¯ϕϕ ⊕

(cid:16)

¯ωµωνdxµ ⊗ dxν(cid:17)

⊕¯ζµνζρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ). (31)

Indicating here with d the differential operator and with
δ the codifferential operator, we define the Dirac oper-
ator D as D = δ + d, that is restricted to the space of
topological bosons. Thus we define the action of D over
|Φ⟩ as

D |Φ⟩ = −∇µωµ ⊕ (∇µϕ − ∇ρζρµ)dxµ
⊕∇µωνdxµ ∧ dxν.

(32)

The metric ˜G induced by the topological matter field
will have structure similar to ˜g that we can write in full
generality as

˜G = G(0) ⊕ [G(1)]µνdxµ ⊗ dxν

⊕[G(2)]µνρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ). (33)

Proceeding as in the warm-up scenario we might wish to
define the metric induced by the topological field as

˜G = ˜g + α

(cid:16)

D |Φ⟩ ⟨Φ| D

(cid:17)

.

(34)

[g(2)]µνρσ =

1
2

(gµρgνσ − gµσgνρ).

(28)

Thus in this general scenario we consider the two covari-
ant topological metrics ˜g and ˜G each given by the direct

sum of metrics between scalars, vectors and bivectors.
As a reference on our notation for this general scenario
we refer the reader to the Table II and the Table III.
In our interpretation of the metric as a quantum density
matrix, this would correspond to density matrix corre-
sponding to a pure state D |Φ⟩. However, if the induced
metric ˜G is interpreted as a density matrix, it is natu-
ral to add further terms in the metric ˜G. These terms
will depend on the topological field and the geometry of
the space which will allow us to describe mixed states.
First, we introduce in ˜G a term proportional to |Φ⟩ ⟨Φ|.
Specifically we introduce a term (m2 + ξR) |Φ⟩ ⟨Φ| where
R is the Ricci scalar and ξ might include the case of con-
formal coupling ξ = (d − 2)/(4(d − 1)). This term can
be also interpreted as a projector. Secondly, we intro-
duce a term depending explicitly on the curvature of the
manifold. Since ˜G involves the metric for scalars, vectors
and bivectors on equal footing, it is natural to consider a
further term involving ˜R given by the direct sum of the
Ricci scalar R, the Ricci tensor of elements Rµν and the
Riemann tensor of elements Rµνρσ, i.e.

˜R = R ⊕

(cid:16)

Rµνdxµ ⊗ dxν(cid:17)

⊕Rµνρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ).

(35)

Including ˜R into the metric ˜G will allow as to describe
more general metric matrices that are not decomposable
into sum of projectors.

From these considerations, it follows that in the in-
duced metric ˜G, we will substitute the term D |Φ⟩ ⟨Φ| D
with ˜M defined as

˜M = D |Φ⟩ ⟨Φ| D + (m2 + ξR) |Φ⟩ ⟨Φ| .

(36)

As we will see in the following paragraph this choice will
allow us to effectively overcome the first limitation of
the warm-up scenario and to recover the Klein-Gordon
equation in curved spacetime in full. Furthermore we
consider also the additional term proportional to ˜R and
we postulate that the metric ˜G induced by the geometry
and the matter fields is given by

˜G = ˜g + α ˜M − β ˜R.

(37)

As we will see in the following the addition of the term
proportional to ˜R will allow also to overcome the second
limitation of the warm-up scenario. Note that here α, β
are positive constants. In particular, since we require ˜G
to be adimensional, we need to consider α = α′ℓd
P and
P where ℓP is the Planck length and α′, β′ are
β = β′ℓ2
adimensional in the units ℏ = c = 1.

In the main body of this paper we will investigate only
(bosonic) Dirac-K¨ahler matter fields. However gauge
fields and fermionic Dirac fields can be included as well.
For a discussion of the inclusion of Abelian gauge field
see Appendix A.

Possibly this approach could be extended to include
also higher-forms. However, for simplicity, we consider

6

here only topological matter fields formed by the direct
sum between a 0-form, a 1-form and a 2-form as this
the minimal choice that will allow us to include in the
action the Ricci scalar, the Ricci and the Riemann tensor
explicitly.

FIG. 1. Schematic representation of this theoretical frame-
work.The metric induced by the matter field ˜G affects the
metric of the manifold ˜g and vice versa the metric of the
manifold affects the metric induced by the matter field. The
considered Lagrangian is given by the quantum relative en-
tropy between the topological metric ˜g of spacetime and the
topological metric induced by the topological matter fields
˜G. Since, by definition, the entropy of the metric vanishes
identically, the quantum relative entropy in the Lagrangian L
reduces to a single term: the quantum cross-entropy.

B. Entropic topological and geometrical action

We propose a statistical mechanics action formulated
in terms of the quantum relative entropy between the
metric ˜g and the metric ˜G induced by the topological
matter fields. In order to define our action we need to ex-
tend the notion of eigenvalues to metric tensors between
bivectors. This will allow to define the entropy and the
quantum relative entropy in this novel framework. For a
detailed discussion of this mathematical background see
Appendix B that constitutes also the reference for our
notation. First of all we observe that the entropy asso-
ciated to the metric ˜g remains zero. Indeed we define ˜H
as

˜H = Tr˜g ln ˜g−1

= 1 ln 1 + Trg ln g−1 + Trg(2) ln g−1

(2) = 0,

(38)

where we have used Eq.(9) and the identity derived in
the Appendix B (in Eq.(B39)),

Trg(2) ln g−1

(2) = 0,

(39)

This equation is a direct consequence of the fact that not
only g but also g(2), has all the eigenvalues equal to one.
We are now in the position to consider the Lagrangian
given by the quantum relative entropy between ˜g and ˜G,

L := −Tr˜g ln ˜g−1 + Tr˜g ln ˜G−1

(40)

(see Figure 1 for an illustration of the physical model
beyond the choice of this Lagrangian). Since we have
˜H = 0 we obtain

L = Tr˜g ln ˜G−1.

(41)

By treating separately the contributions of G(0) G(1) and
G(2) we get the explicit expression for the Lagrangian L
given by

L := ln[G(0)]−1 + Trg ln[G(1)]−1
+Trg(2) ln[G(2)]−1.

7

C.

Introduction of G-field ˜G and the field ˜Θ

In this section our goal is to investigate the property of
the modified gravity emerging from the entropic action.
To this end we introduce the auxiliary G-field ˜G and the
auxiliary field ˜Θ.
In this way we will be able to show
in the following that the proposed entropic action can
be interpreted as the sum of a dressed Einstein-Hilbert
action with an emergent positive cosmological constant
only depending on the G-field ˜G and a matter action.

(42)

As mentioned before we can express the Lagrangian L

Since the metric matrices g(n) have all their eigenvalues
equal to one, using the notation developed in Appendix
B we can express this Lagrangian as well as
L := −TrF ln ˜G˜g−1

= − ln[G(0)] − TrF ln[G(1)]g−1
−TrF ln[G(2)]−1[g(2)]−1.
The resulting statistical mechanics action S associated
to the Lagrangian L is strictly related to the Araki quan-
tum relative entropy [17, 37, 38], and can be formally de-
rived from a mathematical theory of quantum operators
(see Appendix C). Specifically, the considered action is
given by

(43)

(cid:90) (cid:112)| − g|Ldr.

S =

1
ℓd
P

(44)

This action defines a modified theory of gravity. In the
linearised limit α′ ≪ 1, β′ ≪ 1 this action reduces to the
Einstein-Hilbert action with zero cosmological constant
[46, 47] coupled with the scalar topological field. Indeed
in this limit L reduces to

L = 3βR − α ⟨Φ| D˜g−1D |Φ⟩

−α(m2 + ξR)

(cid:16)

|ϕ|2 + ¯ωµωµ + ¯ζ µνζµν

(cid:17)

.

(45)

where

⟨Φ| D˜g−1D |Φ⟩ = |∇ϕ|2 + |∇µωµ|2 +

2

(cid:12)
(cid:12)∇ρζρµ
(cid:12)

(cid:12)
(cid:12)
(cid:12)

given by Eq.(41) as

L = −TrF ln ˜G˜g−1.

(48)

This Lagragian is nonlinear in ˜G and thus in ˜R.

Several modified gravity actions are questioned be-
cause they give rise to theories with derivatives of the
metric higher than two. Such theories can be affected by
the Ostrogradsky instability, however non-linear theories
not suffering from this pathology are also known, most
notably the f (R) theories [20, 22]. Thus an important
question is whether the proposed theory is also affected
by the Ostrogradsky instability or rather, it generalizes
and extends the realm of viable modified gravity theories
beyond the f (R) theories. In particular the Ostrograd-
sky instability can arise when the Lagrangian depends
on derivatives of order higher than two of the fields, and
thus, in the gravitational setting on higher powers of the
curvature ˜R.

In order to tackle this question we observe that the La-
grangian L has an easy expression as it is only dependent
on the product ˜G˜g−1. Thus, by introducing an auxiliary
field ˜Θ and imposing the constraints

˜G˜g−1 = ˜Θ.

(49)

with Lagrangian multipliers ˜G (constituting another aux-
iliary field) that we will call the G-field, we can reduce
our theory to a theory driven by the Lagrangian ˜L given
by

(cid:12)
(cid:12)ϵµνρ∇µων
(cid:12)

(cid:12)
(cid:12)
(cid:12)

2

.

+

(46)

˜L = −TrF ln ˜Θ − TrF ˜G( ˜G˜g−1 − ˜Θ).

(50)

In the interesting limit in which ωµ = 0 and ζµν = 0 and
the topological matter field is only scalar, Eq.(45) reduces
to the widely studied Einstein-Hilbert action with zero
cosmological constant coupled with the scalar field [53],

L = 3βR − α|∇ϕ|2 − α(m2 + ξR)|ϕ|2.

(47)

As already anticipated, this implies, among the other
things, that this framework overcomes the first and the
second limitations of the warm-up scenario.
In fact in
this way we recover the Klein-Gordon Lagrangian in
curved spacetime in full. Moreover, by adding to ˜G the
term proportional to the curvature ˜R we solve the sec-
ond limitation of the warm-up scenario, and we obtain
that the entropic action allows for the full determination
of the metric in the vacuum.

This Lagrangian is now linear in ˜G˜g−1. Note that a
conservative interpretation of this transformation will
not give a physical interpretation to the auxiliary fields.
Thus, according to this point of view, the auxiliary fields
are not changing the physics of the original Lagrangian
and this theory might be prone to Ostrogradsky insta-
bility. However, we known from statistical physics that
Lagrangian multipliers can also acquire a rather physical
meaning. For instance the temperature and the chemical
potential are Lagrangian multipliers that are measurable.
Here we would like to embrace this point of view and give
a physical meaning to the introduced Lagrangian multi-
pliers as physical fields defined on our manifold K. Inter-
preting in this way the Lagrangian multipliers changes
the physics of the problem as the phase space associated

to the equations of motion acquire new dimensions and
the fixed points as well as the initial value problem will
involve the newly introduced fields. In this latter inter-
pretation, introducing the auxiliary fields and giving a
physical meaning to them as encoding for new fields, we
have reduced our theory to a theory linear in ˜R.
In
particular, as we will see below, the equations of motion
will involve at most second order derivatives of the fields,
thus the model might avoid the Ostrogradsky instabil-
ity. A definitive answer to the stability question would
follow from further analysis (for example a Hamiltonian
analysis).

The fields ˜Θ and ˜G are given by

˜Θ = Θ(0) ⊕ Θ(1) ⊕ Θ(2),
˜G = G(0) ⊕ G(1) ⊕ G(2),

(51)

and G(1) having elements [G(1)] ν

with Θ(1) having elements [Θ(1)] ν
[Θ(2)] ρσ
µν
elements [G(2)] ρσ
that is linear in ˜G˜g−1, can be expressed as

µ , Θ(2) having elements
µ , G(2) having
µν . The term W, of the Lagrangian ˜L

fields. By using the definition of ˜G given by Eq.(A1), we
can derive the equation of motion of the matter fields by
considering the variation with respect to ⟨Φ|, getting,

8

D˜g−1

G D |Φ⟩ + ˜g−1

G (m2 + ξR) |Φ⟩ = 0.

Here ˜gG, given by

˜gG = ˜G

−1

g,

(55)

(56)

can be interpreted as the dressed metric which affects the
matter fields. Specifically, g can be seen as a bare metric
and the G-field ˜G
can be seen as a dressing of this
metric that gives rise to the dressed metric ˜gG given by
Eq.(56).

−1

E. Modified gravity

We now turn to the equations for modified gravity con-
sidering variation of our action ˜S with respect to the
metric g and to the fields ˜Θ and ˜G.

W = TrF ˜G( ˜G˜g−1 − ˜Θ) =

2
(cid:88)

n=0

Wn,

(52)

1. Variation with respect to ˜G

with

W0 = G(0)(G(0) − Θ(0)),
W1 = [G(1)] µ
ρ

(cid:16)

W2 = [G(2)] µν

ηθ

(cid:17)

[G(1)]µνgνρ − [Θ(1)] ρ
(cid:16)
[G(2)]µνρσ[g(2)]ρσηθ − [Θ(2)] ηθ

µν

µ

,

The variation with respect to the fields ˜G enforces the
constraints in Eq.(49) which, by using the expression for
˜G given by Eq.(A1), can be expressed explicitly as

(cid:17)

. (53)

˜Θ = ˜I + α ˜M˜g−1 − β ˜R˜g−1,

(57)

Note that the use Lagrange multipliers in the present
theory extends the equivalence between the f (R) the-
ories and Brans-Dicke Theory achieved through a Leg-
endre transformation [20, 22]. However using an exten-
sive number of Lagrange multipliers might be considered
a dangerous mathematical operation. For the sake of
simplicity here we work under the assumption that ˜L is
equivalent to L. Whereas it might be proven that L is not
equivalent to ˜L we assume that our true theory is given
by ˜L which we might always consider as a “canonical”
version of L.

The resulting statistical mechanics action ˜S associated

to the Lagrangian ˜L is given by

(cid:90) (cid:112)| − g| ˜Ldr.

˜S =

1
ℓd
P

(54)

We are now in the position to derive the equations for
the matter fields Φ, the metric gµν and the fields ˜Θ and
˜G by considering the variation of ˜L with respect to these
fields.

D. Equation of motion for the matter fields

Here we consider the action ˜L defined in Eq.(50) de-
pending linearly on ˜G which is encoding for the matter

where ˜I is the (topological) identity. Since α = α′ℓ4
P
and β = β′ℓ2
P in the regime of low energies and low cur-
vatures, we have that ˜Θ is a small perturbation of the
identity ˜I.

Note that these are the equations that determine the
relation between the fields ˜Θ the curvature ˜R and the
matter field determining ˜M. We can write these equa-
tions by separating the contribution corresponding to the
metric for 0-forms, 1-forms and 2-forms obtaining

Θ(0) = 1 + αM(0) − βR,

[Θ(1)] ν
[Θ(2)] ⃗ν

µ = δ ν
⃗µ = δ ⃗ρ

µ + α[M(1)]µρgρν − βRµρgρν,
⃗µ + α[M(2)]⃗µ⃗ρ[g(2)]⃗ρ⃗ν − βR⃗µ⃗ρ[g(2)]⃗ρ⃗ν,

where we have indicated a pair of indices with a vector
symbol, e.g. ⃗µ. Since the trace of the Ricci tensor as
well as the trace of the Riemann tensor, are both equal
to the Ricci scalar, upon performing the trace of these
expressions, we get some constraints on the trace of the
fields Θ(n), i.e.

(cid:33)

(cid:32)

d
n

− TrF Θ(n) + αTrF M(n)g−1

(n) = βR,

(58)

for any n ∈ {0, 1, 2}.

2. Variation with respect to ˜Θ

Thanks to the logarithmic nonlinearity in ˜L the varia-

tion of the action ˜S with respect to ˜Θ simply reads

˜Θ−1 = ˜G.

(59)

Thus we obtain that the field ˜Θ corresponds to the in-
verse of the dressing G-field ˜G. Using Eqs.(57) we find
that the equation of motion for the G-field ˜G is given by

−1

˜G

= ˜I + α ˜M˜g−1 − β ˜R˜g−1,

(60)

and we can simply eliminate the field ˜Θ, from the action.
In this way the considered action ˜S can be decomposed
into two terms as

˜S = βSG + αSM ,

with

SG =

1
ℓd
P

(cid:90) (cid:112)| − g|LGdr, SM =

(cid:90) (cid:112)| − g|LM dr.

1
ℓd
P

(61)

(62)

The Lagrangians LG and LM appearing in the above
definition of SG and SM can be expressed as

(cid:16)

LG =

RG − 2ΛG

(cid:17)

, LM = −MG.

(63)

where RG is the dressed Ricci scalar and MG includes
all dependence with the matter fields |Φ⟩ while ΛG is the
emergent positive cosmological constant. Specifically we
have

RG = TrF ˜g−1
G

˜M ,
˜R, MG = TrF ˜g−1
G
(cid:17)
(cid:16) ˜G − ˜I − ln ˜G

TrF

.

1
2β

ΛG =

9

Let us define the stress-energy tensor T in the usual way
with elements Tµν given by

−

1
(cid:112)| − g|

δSM
dgµν

= Tµν.

(65)

With this notation we can expressed the modified Ein-
stein equations as

RG

(µν) −

(cid:16)

gµν

1
2

(cid:17)

RG − 2ΛG

+ D(µν) = κT(µν),

(66)

where κ = α/β, (µν) indicates symmetrization of the
indices, RG
µν are the elements or the dressed Ricci tensor
given by

RG

µν = G(0)Rµν + [G(1)] ρ
+2[G(2)] ηρ1ρ2

µ

Rρ1ρ2νη,

µ Rρν − [G(2)]ρ1ρ2µηR ηρ1ρ2

ν

(67)

and Dµν are the elements depending on second deriva-
tives of the G-field ˜G given by

Dµν = (∇ρ∇ρgµν − ∇µ∇ν)G(0) − ∇ρ∇ν[G(1)](ρµ)

1
2

∇ρ∇ρ[G(1)]µν +

+
+∇η∇ρ[G(2)]µρνη + ∇ρ∇η[G(2)]ηµρν

∇ρ∇η[G(1)]ρηgµν

1
2

+

1
2

[∇ρ, ∇η][G(2)]ρηµν.

(68)

It follows that the modified Einstein equations involve
only second derivatives of the metric and second deriva-
tives of the field ˜G. However these equations might have
more solutions than the Einstein equations. A detailed
study of the solutions and the viability of these equations
is beyond the scope of this work and will be the subject
of future investigations.

(64)

4. Discussion

From this reformulation of the action ˜S we see that the
Lagrangian LG has a the structure of a dressed Einstein-
Hilbert action and depends on the metric and the G-field
˜G. In particular the Ricci scalar R is substituted to the
dressed Ricci scalar RG and the role of the cosmological
constant is played by ΛG that is non-negative and only
dependent on the G-field ˜G. Whenever this field is close
to the identity, e.g. ˜G ≃ ˜I + ˜ϵ we obtain that ΛG is
positive but very small, i.e.
its first non-trivial term is
quadratic in ˜ϵ. Thus the emergent positive cosmological
constant ΛG is small in this limit and only determined by
the G-field. Finally we recover as already noticed, that
the action ˜S reduces to the Einstein-Hilbert with zero
cosmological constant in the low coupling limit.

In summary the introduction of the G-field turns the
proposed entropy action Eq.(41) into the action Eq.(61)
involving a dressed Einstein-Hilbert action and a dressed
matter action given by Eq.(62) depending on the matter
and the gravity dressed Lagrangians Eq.(63) respectively.
The gravitational dressed action LG displays an emergent
positive cosmological constant ΛG only dependent on the
G-field and given by Eq.(64). The equations of motion
associated to this action involve solving Eqs.(55) for the
matter fields, and Eqs. (60) and Eqs. (66) for the met-
ric and the G-field. All these equations involve at most
second derivatives of the fields.

3. Variation with respect to g

IV. CONCLUSIONS

The modified Einstein equations are obtained by per-
forming the variation of the action ˜S with respect to g.

This work proposes a modified theory of gravity emerg-
ing from statistical mechanics and information theory ac-
tion. The fundamental idea of this theory is to associate

the metric to a quantum operator, playing the role of a
renormalizable and effective density matrix. In particu-
lar two metrics are discussed: the metric of spacetime
that fully defines its geometry and the metric induced
by matter-fields that are effectively curving the space.
The interplay between geometry of spacetime and matter
fields is explicitly captured by the proposed action given
by the quantum relative entropy between the metric and
the metric induced by the matter fields.

Here a Lorentzian theory consistent with this funda-
mental physical interpretation of gravity is formulated.
In order to do this we have built the necessary mathe-
matical background to define the entropy and the cross-
entropy of metric tensors in a Lorentzian well defined
way. A modified gravity is emerging from this frame-
work when the matter fields are described by topological
Dirac-K¨ahler bosons formed by the direct sum between
a 0-form, a 1-form and a 2-form and the induced metric
also depends on the curvature of spacetime. The modified
Einstein equations reduce to the Einstein equations in the
regime of low coupling. By introducing the G-field we ob-
tain the modified Einstein equations and the equations of
motion for the matter and the G-field. From this theory
it emerges that the proposed entropic action takes the
form of a sum between a dressed Einstein-Hilbert action
and a matter action. Interestingly, the dressed Einstein-
Hilbert action displays an emergent positive cosmologi-
cal constant that only depends on the G-field. Moreover,
thanks to the introduction of the G-field, the equations
of modified gravity remains second order in the metric,
in the matter and in the G-field.

The interpretation of the topological metrics tensors as
a quantum operators, or effective density matrix where
we have relaxed the constraints of having unitary trace,
and we have required the existence of the inverse is shown
to be very useful. These choices are motivated here by
the necessity to have a Lorentzian invariant theory. Here
we have established the relation of the adopted quan-
tum relative action with Araki quantum relative entropy
[37], opening the perspective of using the theory of quan-
tum von Neumann algebras and the theory of entangle-
ment [17] to investigate further the properties of the pro-
posed theory.

In conclusion, we hope that this approach can help
identify the deep connections between gravity, quantum
mechanics and statistical physics. Given the interpreta-
tion of the metrics as a quantum operators our hope is
that this approach will also be instrumental to formulate
approaches to quantum gravity in second quantization.
Finally future investigation might explore the role of
the the G-field in dark matter. Future directions in
this line of research involve also the investigation of
the proposed entropic action under the renormalization
group, and possible connections with phenomenology
and experimental results.

This work was partially supported by a grant from the
Simons Foundation. The author would like to thank the

10

Isaac Newton Institute for Mathematical Sciences, Cam-
bridge, for support and hospitality during the programme
Hypergraphs: Theory and Applications, where work on
this paper was undertaken. This work was supported by
EPSRC grant EP/V521929/1.

Appendix A: Inclusion of an Abelian gauge field

An Abelian gauge field Aµ can be easily included in the
general framework introduced in this work. We consider
the operator ˜F defined as

˜F = 0 ⊕ 0µdxµ ⊕ FµνFρσ

(cid:16)

dxµ ∧ dxν(cid:17)

dxρ ∧ dxσ(cid:17)
(cid:16)

,

⊗

where Fµν = ∇µAν −∇νAµ and we consider the following
expression for the metric induced by matter fields

˜G = ˜g + α

(cid:16) ˜M + ˜F

(cid:17)

− β ˜R.

(A1)

Note that in this expression we modify as well the defi-
nition of ˜M as the Dirac operator will be defined as in
Eq.(32) by performing the minimal substitution in the
covariant derivative

∇µ → ∇(A)

µ = ∇µ − ieAµ.

(A2)

Appendix B: Eigenvalues and entropy for metrics
G(1) and for metrics G(n)

In this Appendix our goal is to use algebraic geometry
[54] to define the eigenvalues of the metrics G(n) con-
sidered as quantum operators between n-forms and their
associated entropy. In order to establish the foundation
of this treatment let us revisit the treatment outlined in
Sec. II for defining the eigenvectors and the associated
entropy of the metrics G(1) viewed as quantum opera-
tors between 1-forms and treat on the same footing met-
rics tensor G(n) viewed as quantum operators between
n-forms with arbitrary values of n.

1. Eigenvalues of metric matrices G(n)

A one form can be written as

ω = ωρdxρ.

(B1)

The metric G(1) can be interpreted as a quantum oper-
ator among two of such 1-forms and can be written as

G(1) = [G(1)]µνdxµ ⊗ dxν,

(B2)

where [G(1)]µν is Hermitian. The · product between the
metric G(1) and the generic one form ω is defined as

G(1) · ω = ˆω = ˆωµdxµ,

(B3)

where, by definition

Performing the inner products we thus get

11

ˆωµ := [G(1)]µνωρ ⟨dxν, dxρ⟩ ,

(B4)

where here and in the following ⟨,⟩ indicates the inner
product between n-forms. Thus for canonical 1-forms we
have

⟨dxν, dxρ⟩ = gνρ.

(B5)

Inserting this expression in Eq.(B4) we get,

ˆζµν =

1
2

[G(2)]µνρσζηθ
= [G(2)]µνρσ[g(2)]ρσηθζηθ,

(cid:16)

gρηgσθ − gρθgση(cid:17)

(B14)
where we have used the definition of g(2) given in Eq.(28)
that we rewrite here for convenience,

[g(2)]µνρσ =

1
2

(gµρgνσ − gµσgνρ).

(B15)

ˆωµ = [G(1)]µνgνρωρ.

(B6)

Summarizing we have shown that according to our defi-
nition we have

Summarizing we have shown that according to our defi-
nition we have

G(2) · ζ = [G(2)]µνρσ[g(2)]ρσηθζηθdxµ ∧ dxν.

(B16)

G(1) · ω = [G(1)]µνgνρωρdxµ.

(B7)

The eigenvalue problem of a metric G(1) is then defined
as

G(1) · ω ≡ λω,

or equivalently in matrix form as

[G(1)]µνgνρωρ = λωµ.

(B8)

(B9)

In total analogy with the previous case, the eigenvalue
problem associated to the metric G(2) viewed as quantum
operator among two 2-forms, is defined as

G(2) · ζ ≡ λζ,

(B17)

or equivalently,

[G(2)]µνρσ[g(2)]ρσηθζηθ = λζµν.

(B18)

Note that [G(1)]µν admits also an interpretation as metric
between vectors. We are now in the position to extent
the formalism to the metrics G(2) considered as quantum
operators among two forms of order two. The generic two
form ζ is defined as

ζ = ζηθdxη ∧ dxθ,

(B10)

Note that [G(2)]µνρσ admits also an interpretation as
metric between bivectors. Let us now consider the partic-
ular case in which G(2) = g(2). In this case the eigenvalue
problem Eq.(B18) reads

gµρgνσ − gµσgνρ

(cid:17)(cid:16)

gρηgσθ − gρθgση(cid:17)

ζηθ = λζµν.

(cid:16)

1
4

where ζηθ = −ζθη, i.e. where ζηθ is antisymmetric.

The metric G(2) considered as a quantum operator be-

tween two two-forms is defined as

which has solution

λ = 1,

(B19)

G(2) = [G(2)]µνρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ). (B11)

where G(2) is antisymmetric in the first 2 indices and in
the last 2 indices and Hermitian under the exchange of
the first 2 indices with the second 2 indices. Following a
similar line of reasoning used to define the eigenvalue of
the metric G(1) we define the contraction

G(2) · ζ = ˆζ = ˆζµνdxµ ∧ dxν,

(B12)

where, by definition ˆζµν is defined as

for any arbitrary 2-form associated to the antisymmetric
tensor ζµν. Thus the degeneracy of the eigenvalue is given
by d(d − 1)/2.

The treatment of the eigenvalues associated to the met-
rics tensors G(n) considered as quantum operators be-
tween two n-forms can be performed in a straightfor-
ward way, following similar steps. Let us observe that
the generic n-form is given by

ζ = ζν1ν2...νn dxν1 ∧ dxν2, ∧ . . . ∧ dxνn.

(B20)

ˆζµν :=

1
2

[G(2)]µνρσζηθ

(cid:10)dxρ ∧ dxσ, dxη ∧ dxθ(cid:11) . (B13)

where ζν1ν2...νn is antisymmetric, while the generic ex-
pression for G(n) is given by

G(n) = [G(n)]µ1µ2...µnν1ν2...νn

(dxµ1 ∧ dxµ2 ∧ . . . dxµn ) ⊗ (dxν1 ∧ dxν2, ∧ . . . ∧ dxνn),

(B21)

where G(n) is antisymmetric in the first n indices and in

the last n indices and Hermitian under the exchange of

the first n indices with the second n indices.

For instance, it is instructive to discuss explicitly the

form of the metric g(n) induced on n-forms by g. This
can be immediately shown to be given by

12

g(n) =

n
(cid:89)

i=1

gµiρi(dxµ1 ∧ dxµ2 ∧ . . . dxµn ) ⊗ (dxν1 ∧ dxν2 , ∧ . . . ∧ dxνn ),

(B22)

or, more explicitly, using the antisymmetric properties of the n forms, as

g(n) = [g(n)]µ1µ2...µnν1ν2...νn

(dxµ1 ∧ dxµ2 ∧ . . . dxµn) ⊗ (dxν1 ∧ dxν2, ∧ . . . ∧ dxνn ),

(B23)

with

[g(n)]µ1µ2...µnν1ν2...νn

=

1
n!

δρ1ρ2...ρn
ν1,ν2...νn

n
(cid:89)

i=1

gµiρi .

(B24)

of indices. Using an analogous notation, we define the ·
product between the generic metric G(n) and the n-form
ζ as

Here and in the following we will use the notation
[g(n)]⃗µ⃗ν of indicating the element of this tensor where
⃗µ = (µ1µ2 . . . µn) and ⃗ν = (ν1ν2 . . . νn) indicate n-tuples

with

G(n) · ζ = ˆζ,

(B25)

ˆζ⃗µ :=

1
n!

[G(n)]⃗µ⃗νζ⃗ρ(dxµ1 ∧ dxµ2 ∧ . . . dxµn ) ⟨dxν1 ∧ dxν2, ∧ . . . ∧ dxνn , dxρ1 ∧ dxρ2 ∧ . . . dxρn ⟩ .

(B26)

Thus the eigenvalue problem for G(n) can be written as

[G(n)]⃗µ⃗ν[g(n)]⃗ν⃗ρζ⃗ρ = λζ⃗µ,

(B27)

where here and in the following we have indicated with
⃗µ ⃗ρ and ⃗η tuples of n indices. From this definition of the
eigenvector of a metric between n-forms it follows imme-
diately that the metric tensor g(n) has all eigenvalues λ
equal to one, i.e.

λ = 1,

(B28)

for any arbitrary value of n, with 0 ≤ n ≤ d.

2. Flattening of the metric tensors G(n) and
reduction to a matrix eigenvalue problem

To define the eigenvalues associated to the metric ten-
sor G(1) between 1-forms, we can use a matrix formalism
and define

[N(1)] ν

µ := [G(1)]µρgρν.

(B29)

The eigenvalues of the tensor G(1) are defined as the
eigenvalues of the matrix N(1). Note that now the
multiplication of this latter matrix with itself preserves
Lorentz invariance.

The eigenvalue problem for the metric G(2) Eq.(B18)
can be as well written in matrix form, by considering

(2) and gF

the m × m flattened matrices GF
(2) with m =
d(d − 1)/2 representing the dimension of the basis for the
2-forms defined on the d dimensional manifold K. For
instance, taking the basis {dxµ ∧ dxν} with µ < ν the
flattened matrices GF
(2) and gM
(2) will have respectively
matrix elements

[GF

(2)]

µν;ρσ

= 2[G(2)]µνρσ,

[gF

(2)]

µν;ρσ

= 2[g(2)]µνρσ.

A practical example might be helpful to illustrate this
construction. Assuming that the manifold K is d = 3
dimensional and has three coordinates 0, 1, 2, the flat-
tened matrix gF
(2) associated to g(2), defined in the basis
dx0 ∧ dx(1), dx(0) ∧ dx(2) and dx(1) ∧ dx(2) is given by

gF
(2) =






g00g11 − g01g10 g00g12 − g02g10 g01g12 − g02g11
g00g21 − g01g20 g00g22 − g02g20 g01g22 − g02g21
g10g21 − g11g20 g10g22 − g12g20 g11g22 − g12g21




 .

Using these flattened matrices we then construct the ma-
trix N(2) of matrix elements

[N(2)]

µν

ηθ

:= [GF

(2)]

µνρσ

[gF

(2)]

ρσηθ

,

(B30)

where µ < ν and η < θ. Note that now the usual ma-
trix multiplication of N(2) with itself preserves Lorentz
invariance. The eigenvalues of this matrix N(2) are equal
to the eigenvalue of G(2) defined in Eq.(B18).

Similarly metric tensors G(n) considered as quantum
operators between n-forms can be flattened by consider-
ing a basis of independent n-forms. For instance a basis
for these n-forms can be given by the canonical n-forms

dxµ1 ∧ dxµ2 ∧ . . . ∧ dxµn ,

(B31)

with µ1 < µ2 < . . . < µn. This canonical basis is formed

by m =

n-forms.

(cid:32)

(cid:33)

d
n

On this basis we can define the m × m flattened ma-

trices

13

4. Entropy for metric tensors G(n)

The entropy H of metric tensor G(n) is defined as

H = TrG(n) ln G−1

(n) := −

λ ln λ

(B38)

(cid:88)

λ

where λ indicates the generic eigenvalue of G(n). Since
g(n) has all eigenvalues equal to one, it follows

H(n) = Trg(n) ln g−1

(n) = 0,

(B39)

[GF

(2)]

⃗µ;⃗ν

= n![G(2)]⃗µ;⃗ν,

[gF

(2)]

⃗µ;⃗ν

= n![g(2)]⃗µ;⃗ν.

for any value of 0 ≤ n ≤ d. The cross entropy between
g(n) and G(n) is defined as

Starting from these flattened matrices we define the ma-
trix N(n) of elements

[N(n)]
⃗µ

⃗η

:= [GF

(n)]

⃗µ⃗ρ

[gF

(n)]

⃗ρ⃗η

.

(B32)

As we have seen for n = 1 and n = 2 now these matrices
can be multiplied preserving Lorentz invariance, and the
eigenvalues of these matrices correspond to the eigenval-
ues of the metric tensor G(n).

3. Trace of the metric tensors G(n)

The trace of the metric tensors G(n) is defined as the

trace of the matrix N(n) or equivalently as

TrG(n) = TrM N(n).

(B33)

For ease of notation in the following we will also define
indicate this trace with

TrF G(n)g−1

(n) = TrG(n) = TrM N(n).

(B34)

Trg(n) ln G−1
(n)

:= −TrF ln G(n)g−1
(n)

:= −TrM N(n) = −

ln(µ), (B40)

(cid:88)

µ

where µ indicates the generic eigenvalue of N(n).

Appendix C: The topological metric as a quantum
operator

In this Appendix we outline the underlying quantum
theory of the proposed general scenario and the relation
of the proposed entropy action with the Araki quantum
relative entropy [37, 38].

Our treatment will consider quantum operators in first
quantization. We will provide the foundation of the the-
ory of topological metric tensors interpreted as quantum
operators [33] where the vectors of our Hilbert space are
the topological fields formed by the direct sum of a 0-
form, a 1-form and a 2-form.

We consider the two generic topological fields |Ψ⟩ and

|Φ⟩ given by

From the above definition of N(n) it follows that our def-
inition of the trace is the usual definition of the trace of
a tensor, i.e.,

|Ψ⟩ = ϕ ⊕ ωµdxµ ⊕ ζµνdxµ ∧ dxν,
|Φ⟩ = ˆϕ ⊕ ˆωµdxµ ⊕ ˆζµνdxµ ∧ dxν.

(C1)

TrF G(n)g−1

(n) = [G(n)]⃗µ⃗ρ[g(n)]⃗ρ⃗µ.

(B35)

The scalar product among these two topological fields is
given by

Specifically, for n ∈ {1, 2} we obtain

⟨⟨Ψ, Φ⟩⟩ =

(cid:90) (cid:112)−|g|

(cid:16) ¯ϕ ˆϕ + ¯ωµ ˆωµ + ¯ζµν

ˆζ µν(cid:17)

dr,

(C2)

TrG(1) = [G(1)]µρgρµ,
TrG(2) = [G(2)]µνρσ[g(2)]ρσµν,

(B36)

and for general n we have It follows that the trace of g(n)
are given by

where ˆωµ = gµρ ˆωρ and ˆζ µν = gµρgνσ ˆζρσ = [g(2)]µνρσ ˆζρσ.
Thus the Hilbert space H is endowed with a scalar prod-
uct defined through the default metric tensor ˜g−1 given
by

Trg(n) =

(cid:33)

,

(cid:32)

d
n

(B37)

˜g−1 = 1 ⊕ gµνdxµ ⊗ dxν
⊕[g(2)]µνρσ(cid:16)

dxµ ∧ dxν

(cid:16)

(cid:17)

⊗

dxρ ∧ dxσ

(cid:17)

(C3)

for every 0 ≤ n ≤ d.

This scalar product has the following properties:

• Linearity on the second term

⟨⟨Ψ, c1Φ1 + c2Φ2⟩⟩ = c1 ⟨⟨Ψ, Φ1⟩⟩ + c2 ⟨⟨Ψ, Φ2⟩⟩ , (C4)

for arbitrary c1, c2 ∈ C.

• Antilinearity on the first term

and satisfies
(cid:68)(cid:68)

Ψ, ˜G · Φ

(cid:69)(cid:69)

(cid:68)(cid:68) ˜G⋆ · Ψ⋆, Φ⋆(cid:69)(cid:69)

=

,

⋆

(C13)

for any arbitrary choice of |Ψ⟩ and |Φ⟩. Here the · product
of ˜G⋆ with |Φ⋆⟩ is given by

14

⟨⟨c1Ψ1 + c2Ψ2Φ⟩⟩ = ¯c1 ⟨⟨Ψ1| Φ⟩⟩ + ¯c2 ⟨⟨Ψ2| Φ⟩⟩ , (C5)

for arbitrary c1, c2 ∈ C.

˜G⋆ · |Φ⋆⟩ = [G⋆

(0)]ϕ ⊕ [G⋆

(1)]µνωνdxµ

⊕[G⋆

(2)]µνρσζρσdxµ ∧ dxν.

(C14)

• Scalar product of a topological field with itself The
scalar product of a topological field with itself is
real:

Due to the fact the the metrics G(n) that constitute ˜G
are Hermitian under the exchange of the first n and the
second n indices, we have that ˜G⋆ is related to ˜G by

⟨⟨Ψ, Φ⟩⟩ ∈ R,

(C6)

unless is infinite.

The Hilbert space H is formed by all topological fields
|Φ⟩ such that

where

G⋆
(0) = G(0),
(1)]µν = [G(1)]µν,
[G⋆
(2)]µνρσ = [G(1)]µνρσ,

[G⋆

(C15)

⟨⟨Φ| Φ⟩⟩ < ∞.

(C7)

[G(1)]µν = gµρ[G(1)]ρσgνσ,

The metric induced by the matter field ˜G

˜G = [G(0)] ⊕ [G(1)]µνdxµ ⊗ dxν
dxµ ∧ dxν(cid:17)
⊗

⊕[G(2)]µνρσ

(cid:16)

(cid:16)

dxρ ∧ dxσ(cid:17)

.(C8)

endowed with the · product defined in the Appendix B
(Eq.(B3) and (B12)) can be viewed as a quantum oper-
ator ˜G : H → H where ˜G · |Φ⟩ ∈ H,

˜G · |Φ⟩ = ϕ ⊕ [G(1)]µνωνdxµ

⊕[G(2)]µνρσζ ρσdxµ ∧ dxν.

(C9)

The metric ˜g of the manifold K can be used to define a
dual Hilbert space H⋆ given by the dual topological field.
For instance |Ψ⋆⟩ is the dual of |Ψ⟩ and |Φ⋆⟩ is the dual
of |Φ⟩ with |Ψ⋆⟩ , |Φ⋆⟩ given by

|Ψ⋆⟩ = ϕ ⊕ ωµdxµ ⊕ ζ µνdxµ ∧ dxν,
|Φ⋆⟩ = ˆϕ ⊕ ˆωµdxµ ⊕ ˆζ µνdxµ ∧ dxν,

(C10)

where ωµ = gµρωρ, ˆωµ = gµρ ˆωρ and ζ µν =
[g(2)]µνρσζρσ, ˆζ µν = [g(2)]µνρσ ˆζρσ. While the Hilbert
space H is endowed with a scalar product defined through
the default metric tensor ˜g−1 the Hilbert space H⋆ is en-
dowed with a scalar product ⟨⟨Ψ⋆, Φ⋆⟩⟩⋆ mediated by ˜g
such that

⟨⟨Ψ, Φ⟩⟩ = ⟨⟨Ψ⋆, Φ⋆⟩⟩⋆ .

(C11)

The dual operator ˜G⋆ : H⋆ → H⋆ of ˜G is given by

˜G⋆ = G⋆

(0) ⊕ [G⋆

(1)]µνdxµ ⊗ dxν
(cid:17)

dxµ ∧ dxν

⊕[G⋆

(2)]µνρσ(cid:16)

(cid:16)

⊗

dxρ ∧ dxσ

(cid:17)
.(C12)

[G(2)]µνρσ = [g(2)]µνη1η2 [G(2)]η1η2θ1θ2

[g(2)]θ1θ2ρσ.

Thus we will indicate the relation between ˜G⋆ and ˜G for
short as

˜G⋆ = ˜g−1 ˜G˜g−1.

(C16)

Form this relation it follows that the dual of the default
metric ˜g is the inverse metric ˜g−1, i.e.

˜g⋆ = ˜g−1.

(C17)

Interestingly, the metric tensors are such that the dual
of the dual coincides with the metric tensor itself, indeed
we have

˜G = ˜G⋆⋆ = ˜g ˜G⋆˜g.

(C18)

The topological metrics ˜G and ˜G⋆ that we consider
in this work are respectively elements of the algebras U
and U∗ that generalizes the C ∗ algebra [33] and have the
following properties:

(a) U and U⋆ are algebras with complex numbers as

the coefficient field.

(b) The product between ˜G1, ˜G2 ∈ U given by

˜Gn = G(0),n ⊕ [G(1),n]µνdxµ ⊗ dxν

⊕[G[2],n]µνρσ(dxµ ∧ dxν) ⊗ (dxρ ∧ dxσ),(C19)

for n ∈ {1, 2}, is mediated by the metric ˜g−1, while
the product between ˜G⋆
1, ˜G⋆
2 ∈ U⋆ is mediated by
the metric ˜g. Specifically we have,
˜G1˜g−1 ˜G2 = [G(0),12] ⊕ [G(1),12]µνdxµ ⊗ dxν
dxρ ∧ dxσ(cid:17)
dxµ ∧ dxν(cid:17)

⊗

(cid:16)

(cid:16)

⊕[G(2),12]µνρσ

,

with

where TrF

(cid:16) ˜G ˜G⋆(cid:17)

is given by

15

[G(0),12] = [G(0),1][G(0),2],

[G(1),12]µν = [G(1),1]µη1
[G(2),12]⃗µ⃗ρ = [G(2),1]⃗µ⃗η1

gη1η2[G(1),2]η2ν,
[g(2)]⃗η1,⃗η2 [G(2),2]⃗η2⃗ρ. (C20)

Similarly we have

˜G⋆

1˜g ˜G⋆

2 = [G⋆

(0),12] ⊕ [G⋆
(2),12]µνρσ(cid:16)

⊕[G⋆

(1),12]µνdxµ ⊗ dxν
(cid:16)

(cid:17)

dxµ ∧ dxν

⊗

dxρ ∧ dxσ

(cid:17)

,

(cid:16) ˜G ˜G⋆(cid:17)

TrF

= G2

(0) + [G(1)]µν[G(1)]νµ
+[G(2)]µνρσ[G(2)]ρσµν.

(C26)
For a topological metric ˜G interpreted as a quantum
operator in U we define the square root of the modular
operator ∆1/2
˜G,g

: H → H as

with

∆1/2
˜G,g

(cid:112) ˜G ˜G⋆ = ˜G˜g−1,

=

(C27)

(0),12] = [G⋆
[G⋆
(1),12]µν = [G⋆
(2),12]⃗µ⃗ρ = [G⋆

(0),1][G⋆
(0),2],
(1),1]µη1 gη1η2 [G⋆
[g(2)]⃗η1,⃗η2
(2),1]

⃗µ⃗η1

[G⋆

[G⋆

(1),2]η2ν,
[G⋆

(2),2]⃗η2⃗ρ. (C21)

(c) A bijection ˜G ∈ U → ˜G⋆ ∈ U⋆ and a bijection
˜G⋆ ∈ U⋆ → ˜G⋆⋆ ∈ U are defined and satisfy the
following properties:

(i) The dual of the dual coincides with the metric

tensor itself,
(cid:16) ˜G⋆(cid:17)⋆

= ˜G⋆⋆ = ˜G.

(C22)

where the last identity is derived under the assumption
that ˜G is positively definite, i.e.
it has only positive
eigenvalues. In this assumption the action of the square
root of the modular operator ∆1/2
on the topological
˜G,g
field |Φ⟩ given by Eq.(C1) can be explicitly expressed as

∆1/2
˜G,g

|Φ⟩ = G(0)ϕ ⊕ [G(1)]µρgρνωνdxµ

⊕[G(2)]µνη1η2

gη1η2ρσ
(2)

ζρσ

(cid:16)

dxµ ∧ dxν(cid:17)

.(C28)

(ii) The product between metrics in U maps, un-
der the bijection, to the product between dual
metrics in U⋆ and vice-versa according to:

In terms of the modular operator the considered entropic
action is defined similarly to the usual Araki quantum
relative entropy [37, 38] as

(cid:16) ˜G1˜g−1 ˜G2
(cid:16) ˜G⋆

1˜g ˜G⋆

2

(cid:17)⋆

(cid:17)⋆

= ˜G⋆

2˜g ˜G⋆
1,

= ˜G2˜g−1 ˜G1.

(C23)

S =

1
ℓP

(cid:90) (cid:112)| − g|Ldr,

(C29)

(iii) The dual of a linear combination of metrics
is U and the dual of a linear combination of
metrics in U⋆ obeys:

where

(c1 ˜G1 + c2 ˜G2)⋆ = ¯c1 ˜G⋆
(c1 ˜G⋆

1 + ¯c2 ˜G⋆
2,
2)⋆ = ¯c1 ˜G1 + ¯c2 ˜G2.

1 + c2 ˜G⋆

L = −TrF ln ∆1/2
˜G,g

= −TrF ln ˜G˜g−1.

(C30)

(C24)

(d) The norm associated to the topological metric ˜G ∈
U is equal to the norm associated to the dual and
given by ∥ ˜G∥ = ∥ ˜G⋆∥ defined as

∥ ˜G∥ = ∥ ˜G⋆∥ =

(cid:90) (cid:112)| − g|TrF

(cid:16) ˜G ˜G⋆(cid:17)

dr,

(C25)

Thus the entropic action adopted in this work is strictly
related to the Araki quantum relative entropy [37, 38],
albeit the definition needs to take into account the struc-
ture of the Hilbert space H that is here formed by topo-
logical fields given by the direct sum of a 0-form, with a
1-form and a 2-form.

[1] Jacob D Bekenstein. Black holes and entropy. Physical

9(12):3292, 1974.

Review D, 7(8):2333, 1973.

[2] Jacob D Bekenstein. Generalized second law of ther-
modynamics in black-hole physics. Physical Review D,

[3] Stephen W Hawking. Particle creation by black holes.
Communications in Mathematical Physics, 43(3):199–
220, 1975.

[4] Shinsei Ryu and Tadashi Takayanagi. Aspects of holo-
graphic entanglement entropy. Journal of High Energy
Physics, 2006(08):045, 2006.

[5] Tatsuma Nishioka, Shinsei Ryu, and Tadashi Takayanagi.
Holographic entanglement entropy: an overview. Jour-
nal of Physics A: Mathematical and Theoretical,
42(50):504008, 2009.

[6] Thomas Faulkner, Aitor Lewkowycz, and Juan Malda-
cena. Quantum corrections to holographic entanglement
entropy. Journal of High Energy Physics, 2013(11):1–18,
2013.

[7] Ted Jacobson. Thermodynamics of spacetime:

the
Einstein equation of state. Physical Review Letters,
75(7):1260, 1995.

[8] Sean M Carroll and Grant N Remmen. What is
Physical Review D,

the entropy in entropic gravity?
93(12):124052, 2016.

[9] Ted Jacobson. Entanglement equilibrium and the Ein-
stein equation. Physical Review Letters, 116(20):201101,
2016.

[10] Curtis Callan and Frank Wilczek. On geometric entropy.

Physics Letters B, 333(1-2):55–61, 1994.

[11] Goffredo Chirco, Hal M Haggard, Aldo Riello, and Carlo
Rovelli. Spacetime thermodynamics without hidden de-
grees of freedom. Physical Review D, 90(4):044044, 2014.
[12] Goffredo Chirco and Stefano Liberati. Nonequilibrium
thermodynamics of spacetime: The role of gravitational
dissipation. Physical Review D—Particles, Fields, Grav-
itation, and Cosmology, 81(2):024016, 2010.

[13] Erik Verlinde. On the origin of gravity and the laws of
newton. Journal of High Energy Physics, 2011(4):1–27,
2011.

[14] Gerard’t Hooft. The holographic principle. In Basics and
Highlights in Fundamental Physics, pages 72–100. World
Scientific, 2001.

[15] Leonard Susskind. The world as a hologram. Journal of

Mathematical Physics, 36(11):6377–6396, 1995.

[16] Brian Swingle. Entanglement renormalization and holog-
raphy. Physical Review D—Particles, Fields, Gravita-
tion, and Cosmology, 86(6):065007, 2012.

[17] Edward Witten. APS Medal for Exceptional Achieve-
ment in Research: Invited article on entanglement prop-
erties of quantum field theory. Reviews of Modern
Physics, 90(4):045003, 2018.

[18] Jonathan Sorce. Notes on the type classification of von
arXiv preprint arXiv:2302.01958,

Neumann algebras.
2023.

[19] Thanu Padmanabhan. Thermodynamical aspects of
gravity: new insights. Reports on Progress in Physics,
73(4):046901, 2010.

[20] Thomas P Sotiriou and Valerio Faraoni. f(R) theories of
gravity. Reviews of Modern Physics, 82(1):451–497, 2010.
[21] Thomas P Sotiriou and Stefano Liberati. Metric-affine
f(R) theories of gravity. Annals of Physics, 322(4):935–
966, 2007.

[22] Richard Woodard. Avoiding dark energy with 1/r modifi-
cations of gravity. In The invisible universe: Dark matter
and dark energy, pages 403–433. Springer, 2007.

[23] Emanuele Berti, Enrico Barausse, Vitor Cardoso,
Leonardo Gualtieri, Paolo Pani, Ulrich Sperhake, Leo C
Stein, Norbert Wex, Kent Yagi, Tessa Baker, et al.
Testing general relativity with present and future astro-
physical observations. Classical and Quantum Gravity,
32(24):243001, 2015.

16

[24] Enrico Barausse, Emanuele Berti, Thomas Hertog,
Scott A Hughes, Philippe Jetzer, Paolo Pani, Thomas P
Sotiriou, Nicola Tamanini, Helvi Witek, Kent Yagi, et al.
Prospects for fundamental physics with LISA. General
Relativity and Gravitation, 52:1–33, 2020.

[25] Leor Barack, Vitor Cardoso,

Samaya Nissanke,
Thomas P Sotiriou, Abbas Askar, Chris Belczyn-
ski, Gianfranco Bertone, Edi Bon, Diego Blas, Richard
Brito, et al.
Black holes, gravitational waves and
fundamental physics: a roadmap. Classical and quantum
gravity, 36(14):143001, 2019.

[26] Gianfranco Bertone, Dan Hooper, and Joseph Silk. Par-
ticle dark matter: Evidence, candidates and constraints.
Physics reports, 405(5-6):279–390, 2005.

[27] Carlo Rovelli and Francesca Vidotto. Covariant loop
quantum gravity: an elementary introduction to quan-
tum gravity and spinfoam theory. Cambridge University
Press, 2015.

[28] Jan Ambjørn, Jerzy Jurkiewicz, and Renate Loll. Emer-
gence of a 4D world from causal quantum gravity. Phys-
ical Review Letters, 93(13):131301, 2004.

[29] Alessandro Codello, Roberto Percacci, and Christoph
Rahmede.
Investigating the ultraviolet properties of
gravity with a Wilsonian renormalization group equation.
Annals of Physics, 324(2):414–469, 2009.

[30] Astrid Eichhorn. An asymptotically safe guide to quan-
tum gravity and matter. Frontiers in Astronomy and
Space Sciences, 5:47, 2019.

[31] Daniele Oriti. Approaches to quantum gravity: Toward a
new understanding of space, time and matter. Cambridge
University Press, 2009.

[32] Carlos Barcelo, Stefano Liberati, and Matt Visser. Ana-
logue gravity. Living reviews in relativity, 14:1–159, 2011.
[33] Huzihiro Araki. Mathematical theory of quantum fields.

Oxford University Press, USA, 1999.

[34] Fabio Ciolli, Roberto Longo, and Giuseppe Ruzzi. The
information in a wave. Communications in Mathematical
Physics, 379(3):979–1000, 2020.

[35] Roberto Longo and Feng Xu. Von Neumann entropy in
qft. Communications in Mathematical Physics, 381:1031–
1054, 2021.

[36] Edward Witten. Gravity and the crossed product. Jour-

nal of High Energy Physics, 2022(10):1–28, 2022.

[37] Huzihiro Araki. Relative entropy of states of von Neu-
mann algebras. Publications of the Research Institute for
Mathematical Sciences, 11(3):809–833, 1975.

[38] Masanori Ohya and D´enes Petz. Quantum entropy and
its use. Springer Science & Business Media, 2004.
[39] Vlatko Vedral. The role of relative entropy in quan-
tum information theory. Reviews of Modern Physics,
74(1):197, 2002.

[40] SI Kruglov. Dirac–K¨ahler equation. International Jour-

nal of Theoretical Physics, 41(4):653–687, 2002.

[41] Peter Becher and Hans Joos. The Dirac-K¨ahler equa-
tion and fermions on the lattice. Zeitschrift f¨ur Physik C
Particles and Fields, 15:343–365, 1982.

[42] David Berenstein, Simon Catterall, and PN Lloyd. Stag-
gered bosons and Kahler-Dirac bosons. arXiv preprint
arXiv:2405.03758, 2024.

[43] David Berenstein. Staggered bosons. Physical Review D,

108(7):074509, 2023.

[44] Ginestra Bianconi. Quantum entropy couples matter
with geometry. J. Phys. A: Math. Theor., 57, 2024.

17

[45] Mikio Nakahara. Geometry, topology and physics. CRC

applications. John Wiley & Sons, 2011.

press, 2018.

[46] Albert Einstein. Die feldgleichungen der gravitation.
Sitzungsberichte der K¨oniglich Preußischen Akademie
der Wissenschaften, pages 844–847, 1915.

[47] Sean M Carroll. Spacetime and geometry. Cambridge

University Press, 2019.

[48] Ginestra Bianconi. The mass of simple and higher-order
networks. Journal of Physics A: Mathematical and The-
oretical, 57(1):015001, 2023.

[49] Nicolas Delporte, Saswato Sen, and Reiko Toriumi. Dirac
walks on regular trees. Journal of Physics A: Mathemat-
ical and Theoretical, 2023.

[50] Eduardo A de Souza Neto, Djordje Peric, and David RJ
Owen. Computational methods for plasticity: theory and

[51] Liqun Qi and Ziyan Luo. Tensor analysis: spectral theory

and special tensors. SIAM, 2017.

[52] Esko Keski-Vakkuri, Claus Montonen, and Marco
Panero. Mathematical Methods for Physics: An Intro-
duction to Group Theory, Topology and Geometry. Cam-
bridge University Press, 2022.

[53] Viatcheslav Mukhanov and Sergei Winitzki.

Introduc-
tion to quantum effects in gravity. Cambridge University
Press, 2007.

[54] Paul Renteln. Manifolds, Tensors and Forms. Cambridge

University Press, 2014.

