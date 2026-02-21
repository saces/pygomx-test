# set some defaults

# one of static, shared
ifndef BUILD_MODE
  BUILD_MODE = static
endif

# one of none, colm, goolm, vodozemac
ifndef OLM_FLAVOUR
  OLM_FLAVOUR = colm
endif

ifndef GO_TAGS
  GO_TAGS =
else
  GO_TAGS += ,
endif

ifeq ($(OLM_FLAVOUR),none)
    GO_TAGS += nocrypto
else ifeq ($(OLM_FLAVOUR),colm)
    GO_TAGS += colm
else ifeq ($(OLM_FLAVOUR),goolm)
    GO_TAGS += goolm
else ifeq ($(OLM_FLAVOUR),vodozemac)
    GO_TAGS += vodozemac
else
  $(error unknown OLM_FLAVOUR $(OLM_FLAVOUR))
endif


# calculate configuration matrix

ifeq ($(BUILD_MODE),static)
  build_mode_name=c-archive
  build_mode_ext=a
else ifeq ($(BUILD_MODE),shared)
  build_mode_name=c-shared
  build_mode_ext=so
else
  $(error unknown BUILD_MODE $(BUILD_MODE))
endif

link_list =

ifeq ($(BUILD_MODE),static)
  ifeq ($(OLM_FLAVOUR),colm)
    link_list += olm
  endif
endif


SOURCE_GO=$(shell find ../libmxclient/ -iname "*.go")

ifndef GO_OUTDIR
  GO_OUTDIR = ../pygomx-module
endif

.PHONY:
all: _pygomx.o libmxclient.h
	mkdir -p build/lib
	cp *.so build/lib

_pygomx.o: libmxclient.h build_ffi.py
	python3 build_ffi.py $(link_list)

libmxclient.h: ../libmxclient/go.mod ../libmxclient/go.sum $(SOURCE_GO)
	cd ../libmxclient/ && \
	CGO_ENABLED=1 go build -buildmode=$(build_mode_name) -tags $(GO_TAGS) -o $(GO_OUTDIR)/libmxclient.$(build_mode_ext) .

.PHONY:
clean:
	-rm _pygomx.*
	-rm libmxclient.*
	-rm -r dist/
	-rm -r build/
	-rm -r pygomx_module.egg-info

.PHONY:
install: all
	python setup.py bdist_wheel
	python setup.py install
