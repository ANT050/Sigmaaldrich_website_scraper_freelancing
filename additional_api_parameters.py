def get_additional_product_parameters(products):
    additional_parameters = {
        'operationName': 'PricingAndAvailability',
        'variables': {
            'productNumber': products,
            'quantity': 1
        },
        'query': '''
            query PricingAndAvailability($productNumber: String!, $brand: String, $quantity: Int!,
                 $catalogType: CatalogType, $checkForPb: Boolean, $orgId: String,
                 $materialIds: [String!], $displaySDS: Boolean = false, $dealerId: String,
                 $checkBuyNow: Boolean, $productKey: String, $erp_type: [String!]) {
              getPricingForProduct(input: {
                productNumber: $productNumber, brand: $brand, quantity: $quantity,
                catalogType: $catalogType, checkForPb: $checkForPb, orgId: $orgId,
                materialIds: $materialIds, dealerId: $dealerId, checkBuyNow: $checkBuyNow,
                productKey: $productKey, erp_type: $erp_type
              }) {
                ...ProductPricingDetail
                __typename
              }
            }

            fragment ProductPricingDetail on ProductPricing {
              materialPricing { ...ValidMaterialPricingDetail __typename }
              discontinuedPricingInfo { ...DiscontinuedMaterialPricingDetail __typename }
              dchainMessage
              productInfo { ...ProductInfoMessageDetail __typename }
              __typename
            }

            fragment ValidMaterialPricingDetail on ValidMaterialPricing {
              brand type currency dealerId listPriceCurrency listPrice
              shipsToday freeFreight sdsLanguages catalogType marketplaceOfferId
              marketplaceSellerId materialDescription materialNumber materialId netPrice
              packageSize packageType price isBuyNow product productGroupSBU quantity
              isPBAvailable vendorSKU isBlockedProduct hidePriceMessageKey
              expirationDate availableQtyInStock availabilities { ...Availabilities __typename }
              additionalInfo { ...AdditionalInfo __typename }
              promotionalMessage { ...PromotionalMessage __typename }
              ... @include(if: $displaySDS) { sdsLanguages __typename }
              minOrderQuantity __typename
            }

            fragment Availabilities on MaterialAvailability {
              date key plantLoc quantity displayFromLink displayInquireLink
              messageType contactInfo { contactPhone contactEmail __typename }
              availabilityOverwriteMessage {
                messageKey messageValue messageVariable1 messageVariable2 messageVariable3 __typename
              }
              supplementaryMessage {
                messageKey messageValue messageVariable1 messageVariable2 messageVariable3 __typename
              }
              __typename
            }

            fragment AdditionalInfo on CartAdditionalInfo {
              carrierRestriction unNumber tariff casNumber jfcCode pdcCode __typename
            }

            fragment PromotionalMessage on PromotionalMessage {
              messageKey messageValue messageVariable1 messageVariable2 messageVariable3 __typename
            }

            fragment DiscontinuedMaterialPricingDetail on DiscontinuedMaterialPricing {
              errorMsg paramList hideReplacementProductLink displaySimilarProductLabel
              hideTechnicalServiceLink replacementProducts { ...ReplacementProductDetail __typename }
              alternateMaterials { ...AlternateMaterialDetail __typename }
              __typename
            }

            fragment ReplacementProductDetail on Product {
              productNumber name description sdsLanguages
              images { mediumUrl altText __typename }
              brand { key erpKey name logo { smallUrl altText __typename } __typename }
              __typename
            }

            fragment AlternateMaterialDetail on Material { number __typename }

            fragment ProductInfoMessageDetail on ProductInfoMessage {
              productNumber messageType message __typename
            }
        '''
    }

    return additional_parameters
